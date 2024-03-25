from django import forms
from .models import User

class UserCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'Telefon',
            'Pesel', 'Data_urodzenia', 'Plec', 'pracownik']
        
        widgets = { 'Data_urodzenia': (forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))}
        
        labels = {
            'username': 'Login',
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'Telefon': 'Telefon',
            'Pesel': 'Pesel',
            'Data_urodzenia': 'Data urodzenia',
            'Plec': 'Płeć',
            'pracownik': 'Pracownik',
        }

class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_deleted']
        labels = {'is_deleted': 'Usuń'}