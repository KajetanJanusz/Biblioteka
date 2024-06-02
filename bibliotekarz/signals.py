from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ksiazki, Rejestracje, User
from datetime import datetime

@receiver(post_save, sender=Ksiazki)
def create_rejestracja(sender, instance, created, **kwargs):
    if created:
        Rejestracje.objects.create(KsiazkaID=instance, Data=datetime.now(), PracownikID=instance.Utworzone_przez)

@receiver(post_save, sender=Ksiazki)
def assign_available_status(sender, instance, created, **kwargs):
    if created:
        instance.Liczba_dostepnych_egzemplarzy = instance.Liczba_egzamplarzy
        instance.Stan = 'Dostępna'
        instance.save(update_fields=['Liczba_dostepnych_egzemplarzy', 'Stan'])

post_save.connect(create_rejestracja, sender=Ksiazki)
post_save.connect(assign_available_status, sender=Ksiazki)
