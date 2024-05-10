from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Permissions

@receiver(post_save, sender=User)
def create_permission(sender, instance, created, **kwargs):
    if created:
        Permissions.objects.create(User=instance)