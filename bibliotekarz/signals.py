from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ksiazki, Rejestracje
from datetime import datetime

@receiver(post_save, sender=Ksiazki)
def create_rejestracja(sender, instance, created, **kwargs):
    if created:
        print('elo')
        Rejestracje.objects.create(KsiazkaID=instance, Data=datetime.now(), PracownikID=instance.PracownikID)

post_save.connect(create_rejestracja, sender=Ksiazki)