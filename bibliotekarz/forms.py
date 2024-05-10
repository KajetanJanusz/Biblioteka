from django import forms
from .models import Ksiazki, Wypozyczenia

class RegisterBookForm(forms.ModelForm):
    class Meta:
        model = Ksiazki
        exclude = ['Stan']

class RentBookForm(forms.ModelForm):
    class Meta:
        model = Wypozyczenia
        fields = ['KlientID']
