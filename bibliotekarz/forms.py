from django import forms
from .models import Ksiazki, Wypozyczenia

class RegisterBookForm(forms.ModelForm):
    class Meta:
        model = Ksiazki
        exclude = ['Stan', 'Utworzone_przez', 'Liczba_dostepnych_egzemplarzy']

class RentBookForm(forms.ModelForm):
    class Meta:
        model = Wypozyczenia
        fields = ['KlientID']

class ExtendRentalForm(forms.ModelForm):
    class Meta:
        model = Wypozyczenia
        fields = ['Data_zwrotu']

        widgets = { 'Data_zwrotu': (forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))}
