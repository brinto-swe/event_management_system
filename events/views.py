from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.utils import timezone
from django.db.models import Count, Q
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from .models import Event, Category, RSVP
from .forms import SignUpForm, EventForm, CategoryForm
from .helpers import in_groups_required

# ---------- Auth ----------
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # is_active=False
            messages.success(request, "Signup successful! Check your email to activate your account.")
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated. Please login.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid or expired.")
        return redirect('signup')

@login_required
def post_login_redirect(request):
    # Role অনুযায়ী dashboard
    if request.user.is_superuser or request.user.groups.filter(name='Admin').exists():
        return redirect('admin_dashboard')
    if request.user.groups.filter(name='Organizer').exists():
        return redirect('organizer_dashboard')
    return redirect('participant_dashboard')

def home_redirect(request):
    # Home = event list (public view)
    return redirect('event_list')

# ---------- Dashboards ----------
@login_required
@in_groups_required('Admin')
def admin_dashboard(request):
    today = timezone.localdate()
    stats = {
        'total_events': Event.objects.count(),
        'total_users': User.objects.count(),
        'upcoming_events': Event.objects.filter(date__gte=today).count(),
        'past_events': Event.objects.filter(date__lt=today).count(),
    }
    todays_events = Event.objects.filter(date=today).select_related('category').annotate(participant_count=Count('attendees'))
    return render(request, 'dashboards/admin_dashboard.html', {'stats': stats, 'todays_events': todays_events})

@login_required
@in_groups_required('Organizer','Admin')
def organizer_dashboard(request):
    today = timezone.localdate()
    # Organizer সব ইভেন্টই ম্যানেজ করতে পারবে (প্রশ্ন অনুযায়ী)
    stats = {
        'total_events': Event.objects.count(),
        'upcoming_events': Event.objects.filter(date__gte=today).count(),
        'past_events': Event.objects.filter(date__lt=today).count(),
    }
    todays_events = Event.objects.filter(date=today).select_related('category').annotate(participant_count=Count('attendees'))
    return render(request, 'dashboards/organizer_dashboard.html', {'stats': stats, 'todays_events': todays_events})

@login_required
def participant_dashboard(request):
    # ইউজার যেগুলোতে RSVP করেছে
    my_events = Event.objects.filter(rsvps__user=request.user).select_related('category').annotate(participant_count=Count('attendees'))
    return render(request, 'dashboards/participant_dashboard.html', {'my_events': my_events})

# ---------- Events ----------
def event_list(request):
    q = request.GET.get('q')
    category_id = request.GET.get('category')
    date_from = request.GET.get('from')
    date_to = request.GET.get('to')

    events = (Event.objects
              .select_related('category')
              .prefetch_related('rsvps__user')
              .annotate(participant_count=Count('attendees', distinct=True))
              .order_by('date', 'time'))

    if q:
        events = events.filter(Q(name__icontains=q) | Q(location__icontains=q))
    if category_id:
        events = events.filter(category_id=category_id)
    if date_from and date_to:
        events = events.filter(date__range=[date_from, date_to])

    categories = Category.objects.all()

    can_add_event = False
    if request.user.is_authenticated:
        # Admin বা Organizer রোল
        can_add_event = request.user.is_superuser or request.user.groups.filter(name__in=['Admin','Organizer']).exists()

    return render(request, 'events/event_list.html', {
        'events': events,
        'categories': categories,
        'can_add_event': can_add_event,
    })

def event_detail(request, pk):
    event = get_object_or_404(
        Event.objects.select_related('category').prefetch_related('rsvps__user'),
        pk=pk
    )
    user_has_rsvped = RSVP.objects.filter(user=request.user, event=event).exists() if request.user.is_authenticated else False
    return render(request, 'events/event_detail.html', {
        'event': event,
        'user_has_rsvped': user_has_rsvped
    })

@login_required
@in_groups_required('Organizer','Admin')
def event_create(request):
    form = EventForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Event created.')
        return redirect('event_list')
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Add Event'})

@login_required
@in_groups_required('Organizer','Admin')
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, request.FILES or None, instance=event)
    if form.is_valid():
        form.save()
        messages.success(request, 'Event updated.')
        return redirect('event_detail', pk=pk)
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Edit Event'})

@login_required
@in_groups_required('Admin','Organizer')  # প্রশ্নে admin পূর্ণ ক্ষমতা; organizer events/categories delete করতে পারে
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted.')
        return redirect('event_list')
    return render(request, 'events/confirm_delete.html', {'object': event, 'type': 'Event'})

# ---------- Categories ----------
@login_required
@in_groups_required('Organizer','Admin')
def category_list(request):
    categories = Category.objects.all().annotate(event_count=Count('events'))
    return render(request, 'events/category_list.html', {'categories': categories})

@login_required
@in_groups_required('Organizer','Admin')
def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Category created.')
        return redirect('category_list')
    return render(request, 'events/category_form.html', {'form': form, 'title': 'Add Category'})

@login_required
@in_groups_required('Organizer','Admin')
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        messages.success(request, 'Category updated.')
        return redirect('category_list')
    return render(request, 'events/category_form.html', {'form': form, 'title': 'Edit Category'})

@login_required
@in_groups_required('Admin','Organizer')  # প্রশ্নে admin group delete পারবে; organizer category delete পারবে
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted.')
        return redirect('category_list')
    return render(request, 'events/confirm_delete.html', {'object': category, 'type': 'Category'})

# ---------- RSVP ----------
@login_required
def rsvp_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    try:
        RSVP.objects.create(user=request.user, event=event)
        messages.success(request, f"RSVP successful for {event.name}. Confirmation email has been sent.")
    except IntegrityError:
        messages.info(request, "You have already RSVP’d for this event.")
    return redirect('event_detail', pk=pk)

@login_required
def my_rsvps(request):
    events = (Event.objects.filter(rsvps__user=request.user)
              .select_related('category')
              .annotate(participant_count=Count('attendees')))
    return render(request, 'events/my_rsvps.html', {'events': events})

def participant_dashboard(request):
    events = Event.objects.filter(rsvps__user=request.user).distinct()
    return render(request, 'dashboards/participant_dashboard.html', {
        'events': events,
    })
