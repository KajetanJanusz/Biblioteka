from typing import Any
from django import forms
from .models import Ksiazki, Wypozyczenia
from datetime import date

class RegisterBookForm(forms.ModelForm):
    class Meta:
        model = Ksiazki
        exclude = ['Stan', 'Utworzone_przez', 'Liczba_dostepnych_egzemplarzy']

class RentBookForm(forms.ModelForm):
    class Meta:
        model = Wypozyczenia
        fields = ['KlientID', 'Data_zwrotu']

        widgets = { 
            'Data_zwrotu': forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})
        }

    def clean(self):
        super(RentBookForm, self).clean()
        
        data = self.cleaned_data.get('Data_zwrotu')

        if data < date.today():
            raise forms.ValidationError('Data musi być pózniejsza od dzisiejszej')
        
        return self.cleaned_data
    

class ExtendRentalForm(forms.ModelForm):
    class Meta:
        model = Wypozyczenia
        fields = ['Data_zwrotu']

        widgets = { 'Data_zwrotu': (forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))}
