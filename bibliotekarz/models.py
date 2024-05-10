from typing import Iterable
from django.db import models
from uzytkownicy.models import User


class Gatunki(models.Model):
    Nazwa = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.Nazwa

class Ksiazki(models.Model):

    Stany = [
        ('Dostępna','Dostępna'),
        ('Wypożyczona','Wypozyczona')
    ]

    Tytul = models.CharField(max_length=100, null=False)
    Autor = models.CharField(max_length=50, null=False)
    Gatunek = models.ForeignKey(Gatunki, on_delete=models.CASCADE)
    Liczba_stron = models.IntegerField()
    Wydawnictwo = models.CharField(max_length=50)
    Rok_wydania = models.IntegerField()
    Cena = models.DecimalField(decimal_places=2, max_digits=5)
    Liczba_egzamplarzy = models.IntegerField()
    Opis = models.CharField(max_length=1000)
    Stan = models.CharField(choices=Stany, max_length=20)
    
    def __str__(self) -> str:
        return self.Tytul


class Wypozyczenia(models.Model):
    Stany =[
        (0,'Nowe'),
        (1,'Przedłużone'),
        (2,'Po terminie'),
        (3,'Zakończone')
    ]

    Data = models.DateField(null=False)
    Data_zwrotu = models.DateField(null=False)
    Stan = models.IntegerField(choices=Stany)
    KsiazkaID = models.ForeignKey(Ksiazki, on_delete=models.CASCADE)
    PracownikID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pracownik')
    KlientID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='klient')
    
    def get_stan_display(self):
        return dict(self.Stany)[self.Stan]
    
    def __str__(self) -> str:
        return f'{self.KsiazkaID.Tytul} wypożyczony dla {self.KlientID.first_name}'


class Rejestracje(models.Model):
    KsiazkaID = models.ForeignKey(Ksiazki, on_delete=models.CASCADE)
    Data = models.DateField(null=False)
    PracownikID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pracownik_rejestracje')

    def __str__(self) -> str:
        return self.KsiazkaID.Tytul