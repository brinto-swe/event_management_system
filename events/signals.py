from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

from .models import RSVP, CustomUser

# Ensure Groups exist
def ensure_groups():
    for name in ['Admin', 'Organizer', 'Participant']:
        Group.objects.get_or_create(name=name)

@receiver(post_save, sender=CustomUser)
def on_user_created_send_activation(sender, instance: User, created, **kwargs):
    ensure_groups()
    if created:
        # Default role: Participant
        participant_group = Group.objects.get(name='Participant')
        instance.groups.add(participant_group)

        instance.is_active = False
        instance.save(update_fields=['is_active'])
        
        # Send activation email
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        token = default_token_generator.make_token(instance)
        activation_link = f"{getattr(settings, 'SITE_URL', 'http://localhost:8000')}{reverse('activate', args=[uid, token])}"
        subject = "Activate your EventMS account"
        message = f"Hi {instance.first_name or instance.username},\n\nPlease activate your account:\n{activation_link}\n\nThanks."
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.email], fail_silently=False)

@receiver(post_save, sender=RSVP)
def on_rsvp_send_email(sender, instance: RSVP, created, **kwargs):
    if created:
        user = instance.user
        event = instance.event
        subject = f"RSVP Confirmed: {event.name}"
        message = (
            f"Hi {user.first_name or user.username},\n\n"
            f"You have successfully RSVP’d to '{event.name}' on {event.date} at {event.time}.\n"
            f"Location: {event.location}\n\nSee you there!"
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
