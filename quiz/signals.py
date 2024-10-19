# quiz/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


# Signal to automatically create a Profile when a new User is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # Use get_or_create to avoid duplicate profile creation
        Profile.objects.get_or_create(user=instance)


# Signal to automatically save the Profile whenever the User is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # Save the profile only if it exists
    if hasattr(instance, "profile"):
        instance.profile.save()
