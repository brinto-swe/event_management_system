from django.db import models
from django.contrib.auth.models import AbstractUser

def default_event_image_path():
    return 'events/defaults/event_default.png'

def default_profile_image_path():
    return 'users/defaults/profile_default.png'

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='users/images/', default=default_profile_image_path, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.username

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
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='organized_events')
    attendees = models.ManyToManyField(CustomUser, through='RSVP', related_name='rsvp_events', blank=True)

    def __str__(self):
        return self.name

class RSVP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rsvps')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} → {self.event.name}"
