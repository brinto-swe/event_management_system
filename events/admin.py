from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Category, Event, RSVP

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_picture', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('profile_picture', 'phone_number')}),
    )

# আগের register করা অংশ
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
