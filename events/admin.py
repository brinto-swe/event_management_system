from django.contrib import admin
from .models import Category, Event, RSVP

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'date', 'time', 'location')
    list_filter = ('category', 'date')

@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event', 'created_at')
    list_filter = ('event', 'created_at')
    search_fields = ('user__username', 'event__name')
