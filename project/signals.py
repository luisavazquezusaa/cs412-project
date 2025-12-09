# File: signals.py
# Author: Luisa Vazquez Usabiaga
# Last updated: 12/09/2025
# Description:
#   Automatically creates a corresponding UserProfile whenever a new Django User 
#   is registered. 


from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    """
    Creates an associated UserProfile whenever a new User object is created.
    This keeps authentication data (User) and application data (UserProfile)
    synchronized.
    """
    if created:
        UserProfile.objects.create(
            user=instance,
            display_name=instance.username,
            email=instance.email
        )
