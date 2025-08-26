from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Event, RSVP, CustomUser, Category
from .forms import EventForm, RSVPForm, CustomUserChangeForm, CustomUserCreationForm, CategoryForm
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .helpers import in_groups_required
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()

# ------------------------ FUNCTION-BASED VIEWS (Auth + Dashboards) ------------------------

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Signup successful! Please login.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "✅ Your account has been activated! You can now log in.")
        return redirect('login')
    else:
        messages.error(request, "❌ Activation link is invalid or expired.")
        return render(request, 'registration/activation_invalid.html')

@login_required
def post_login_redirect(request):
    user = request.user
    if user.is_superuser:
        return redirect('admin_dashboard')
    if user.groups.filter(name='Organizer').exists():
        return redirect('organizer_dashboard')
    return redirect('participant_dashboard')

def home_redirect(request):
    return redirect('event_list')

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
    todays_events = Event.objects.filter(date=today).select_related('category').annotate(participant_count=Count('rsvps'))
    return render(request, 'dashboards/admin_dashboard.html', {'stats': stats, 'todays_events': todays_events})

@login_required
@in_groups_required('Organizer','Admin')
def organizer_dashboard(request):
    today = timezone.localdate()
    stats = {
        'total_events': Event.objects.count(),
        'upcoming_events': Event.objects.filter(date__gte=today).count(),
        'past_events': Event.objects.filter(date__lt=today).count(),
    }
    todays_events = Event.objects.filter(date=today).select_related('category').annotate(participant_count=Count('rsvps'))
    return render(request, 'dashboards/organizer_dashboard.html', {'stats': stats, 'todays_events': todays_events})

@login_required
def participant_dashboard(request):
    my_events = Event.objects.filter(rsvps__user=request.user).select_related('category').annotate(participant_count=Count('rsvps'))
    return render(request, 'dashboards/participant_dashboard.html', {'my_events': my_events})

# ------------------------ PROFILE ------------------------

@login_required
def profile_view(request):
    return render(request, 'profile/profile.html')

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'profile/edit_profile.html', {'form': form})

# ------------------------ PASSWORD (CBV) ------------------------

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "registration/change_password.html"
    success_url = reverse_lazy("password_change_done")

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "registration/change_password_done.html"

class CustomPasswordResetView(PasswordResetView):
    template_name = "registration/password_reset.html"
    email_template_name = "registration/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"

# ------------------------ EVENT (CBV) ------------------------

class EventListView(ListView):
    model = Event
    template_name = "events/event_list.html"
    context_object_name = "events"
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Add category list for filter
        context['categories'] = Category.objects.all()
        # Role-based add button visibility
        context['can_add_event'] = user.is_authenticated and (user.is_superuser or user.groups.filter(name='Organizer').exists())
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = "events/event_detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['rsvp_form'] = RSVPForm()
            context['user_has_rsvped'] = RSVP.objects.filter(user=user, event=self.object).exists()
        else:
            context['user_has_rsvped'] = False
        context['rsvps'] = self.object.rsvps.all()
        return context

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"
    success_url = reverse_lazy("event_list")

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, "Event created successfully!")
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"
    success_url = reverse_lazy("event_list")

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.organizer or self.request.user.is_superuser

    def form_valid(self, form):
        messages.success(self.request, "Event updated successfully!")
        return super().form_valid(form)

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = "events/event_confirm_delete.html"
    success_url = reverse_lazy("event_list")

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.organizer or self.request.user.is_superuser

# ------------------------ CATEGORIES (Function-based) ------------------------

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
@in_groups_required('Admin','Organizer')
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted.')
        return redirect('category_list')
    return render(request, 'events/confirm_delete.html', {'object': category, 'type': 'Category'})

# ------------------------ RSVP (CBV) ------------------------

class RSVPCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        RSVP.objects.get_or_create(user=request.user, event=event)
        messages.success(request, "You have successfully RSVP’d to this event.")
        return redirect("event_detail", pk=pk)

    def get(self, request, pk):
        return redirect("event_detail", pk=pk)

class MyEventsView(LoginRequiredMixin, ListView):
    model = RSVP
    template_name = "events/my_rsvps.html"
    context_object_name = "rsvps"

    def get_queryset(self):
        return RSVP.objects.filter(user=self.request.user)

# ------------------------ USER (CBV) ------------------------

class UserRegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("event_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data.get("username"),
            password=form.cleaned_data.get("password1"),
        )
        login(self.request, user)
        return response

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile/profile.html"

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "profile/edit_profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user

"""
@in_groups_required('Admin', 'Organizer')
def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event_detail.html', {'event': event})

@in_groups_required('Admin', 'Organizer')
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

@in_groups_required('Admin', 'Organizer')
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form})

@in_groups_required('Admin', 'Organizer')
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('event_list')
    return render(request, 'event_confirm_delete.html', {'event': event})
"""