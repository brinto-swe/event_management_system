from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def default_event_image_path():
    # Media root এর ভেতরে ডিফল্ট ফাইল path (ফাইল না থাকলেও error দেবে না)
    return 'events/defaults/event_default.png'

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    image = models.ImageField(upload_to='events/images/', default=default_event_image_path, blank=True)

    # ManyToMany via RSVP
    attendees = models.ManyToManyField(User, through='RSVP', related_name='rsvp_events', blank=True)

    def __str__(self):
        return self.name

class RSVP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rsvps')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  # একই event-এ একই user বারবার RSVP করতে পারবে না
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} → {self.event.name}"
