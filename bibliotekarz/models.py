from typing import Iterable
from django.db import models
from uzytkownicy.models import User
from django.core.exceptions import ValidationError

def positive_decimal(input):
    if input < 0:
        raise ValidationError('Cena ujemna')


class Gatunki(models.Model):
    Nazwa = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.Nazwa

class Ksiazki(models.Model):

    Stany = [
        ('Dostępna','Dostępna'),
        ('Wypożyczona','Wypozyczona')
    ]

    Tytul = models.CharField(max_length=100, null=False, unique=True)
    Autor = models.CharField(max_length=50, null=False)
    Gatunek = models.ForeignKey(Gatunki, on_delete=models.CASCADE)
    Liczba_stron = models.PositiveIntegerField()
    Wydawnictwo = models.CharField(max_length=50)
    Rok_wydania = models.PositiveIntegerField()
    Cena = models.DecimalField(decimal_places=2, null=False, validators=[positive_decimal], max_digits=5)
    Liczba_egzamplarzy = models.PositiveIntegerField()
    Liczba_dostepnych_egzemplarzy = models.PositiveIntegerField()
    Opis = models.CharField(max_length=1000)
    Stan = models.CharField(choices=Stany, max_length=20)
    Utworzone_przez = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.Tytul


class Wypozyczenia(models.Model):
    Stany =[
        ('Nowe','Nowe'),
        ('Przedłużone','Przedłużone'),
        ('Po terminie','Po terminie'),
        ('Zakończone','Zakończone')
    ]

    Data = models.DateField(null=False)
    Data_zwrotu = models.DateField(null=True, blank=True)
    Stan = models.CharField(choices=Stany, max_length=100)
    KsiazkaID = models.ForeignKey(Ksiazki, on_delete=models.CASCADE)
    PracownikID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pracownik')
    KlientID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='klient')

    def get_rent_period(self):
        return self.Data_zwrotu - self.Data

    def __str__(self) -> str:
        return f'{self.KsiazkaID.Tytul} wypożyczony dla {self.KlientID.first_name}'



class Rejestracje(models.Model):
    KsiazkaID = models.ForeignKey(Ksiazki, on_delete=models.CASCADE)
    Data = models.DateField(null=False)
    PracownikID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pracownik_rejestracje')

    def __str__(self) -> str:
        return self.KsiazkaID.Tytul