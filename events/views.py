from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm
from django.db.models import Count
from django.utils import timezone
from django.utils.timezone import localdate

# Create your views here.
def home(request):
    return render(request, "navbar.html")

def dashboard(request):
    today = localdate()

    total_participants = Participant.objects.count()
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gt=today).count()
    past_events = Event.objects.filter(date__lt=today).count()
    todays_events = Event.objects.filter(date=today)

    context = {
        'total_participants': total_participants,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'todays_events': todays_events
    }

    return render(request, 'dashboard.html', context)

# =================== EVENT VIEWS =====================

def event_list(request):
    events = Event.objects.select_related('category').prefetch_related('participants')

    # Filtering by category
    category_id = request.GET.get('category')
    if category_id:
        events = events.filter(category_id=category_id)

    # Filtering by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])

    # Annotate participant count for each event
    events = events.annotate(num_participants=Count('participants'))

    # Total participants across all events
    total_participants = Participant.objects.count()

    categories = Category.objects.all()
    return render(request, 'events/event_list.html', {
        'events': events,
        'total_participants': total_participants,
        'categories': categories
    })

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    participants = event.participants.all()
    return render(request, 'events/event_detail.html', {'event': event, 'participants': participants})



def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/confirm_delete.html', {'object': event, 'type': 'Event'})

# =================== PARTICIPANT VIEWS =====================

def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = ParticipantForm()
    return render(request, 'events/participant_form.html', {'form': form})

def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'events/participant_form.html', {'form': form})

def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        participant.delete()
        return redirect('event_list')
    return render(request, 'events/confirm_delete.html', {'object': participant, 'type': 'Participant'})

# =================== CATEGORY VIEWS =====================

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'events/category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = CategoryForm()
    return render(request, 'events/category_form.html', {'form': form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'events/category_form.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('event_list')
    return render(request, 'events/confirm_delete.html', {'object': category, 'type': 'Category'})
