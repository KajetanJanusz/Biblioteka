from celery import shared_task, Celery
from django.utils import timezone
from .models import Wypozyczenia

@shared_task
def update_rental_status_task():
    now = timezone.now().date()
    expired_rentals = Wypozyczenia.objects.filter(Data_zwrotu__lt=now, Stan__ne=3)
    expired_rentals.update(Stan=2)
