from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_pesel, regex_telefon, regex_pesel, replace, password_validator
from django.core.exceptions import ValidationError
from datetime import datetime

class User(AbstractUser):
    choices = [(0, 'Męźczyzna'),
               (1, 'Kobieta')]

    Telefon = models.CharField(max_length=9,null=False, validators=[regex_telefon])
    # Adres_ID = models.OneToOneField(Adres, on_delete=models.CASCADE, null=False)
    Pesel = models.CharField(max_length=11, unique=True, null=False, validators=[regex_pesel, validate_pesel])
    Data_urodzenia = models.DateField(null = False)
    password_db = models.CharField(max_length=15, null=False, blank=False, validators=[password_validator])
    generated_password = models.CharField(max_length=15, null=False, blank=False, validators=[password_validator])
    Plec = models.IntegerField(choices=choices, null=False)
    pracownik = models.BooleanField(default = False)
    utworzony = models.DateTimeField(auto_now_add=True)
    edytowany = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['Telefon', 'Pesel', 'Data_urodzenia', 'Plec']

    def clean(self):
        super().clean()

        #unikalny email
        email = User.objects.filter(email=self.email).exclude(username=self.username).exclude(is_deleted=True)
        if email.exists():
            print(email)
            raise ValidationError('Ten email jest już w bazie')

        # walidacja oparta o płeć
        if ((self.Plec == 0) and int(self.Pesel[-2])%2 == 0) or ((self.Plec == 1) and int(self.Pesel[-2])%2 != 0):
            raise ValidationError('Pesel nie zgadza się z płcią')

        # walidacja oparta o datę urodzenia
        if self.Data_urodzenia.year > 1900 and self.Data_urodzenia < datetime.today().date():
            poczatek_peselu = self.Data_urodzenia.strftime('%Y%m%d')[2:]

            if self.Data_urodzenia.year > 1999:
                if poczatek_peselu[2] == '0':
                    poczatek_peselu = replace(poczatek_peselu, 2, '2')
                elif poczatek_peselu[2] == '1':
                    poczatek_peselu = replace(poczatek_peselu, 2, '3')
            
            pesel = self.Pesel[:6]

            if poczatek_peselu != pesel:
                raise ValidationError('Pesel niepoprawny do daty urodzenia')
        else:
            raise ValidationError('Pesel nie jest prawidłowy')
        
    def save(self, *args, **kwargs):
        #zmiana zapisu loginu i maila
        self.username = self.username.lower().capitalize()
        self.email = self.email.lower()
        return super(User, self).save(*args, **kwargs)
    


class Permissions(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Add_books = models.BooleanField(verbose_name="Dodawanie książek", default=False)
    Delete_books = models.BooleanField(verbose_name="Usuwanie książek", default=False)
    Edit_books = models.BooleanField(verbose_name="Edytowanie książek", default=False)
    Detail_book = models.BooleanField(verbose_name="Detale książki", default=False)
    Add_user = models.BooleanField(verbose_name="Dodawanie użytkownika", default=False)
    Delete_user = models.BooleanField(verbose_name="Usuwanie użytkownika", default=False)
    Edit_user = models.BooleanField(verbose_name="Edytowanie użytkownika", default=False)
    List_user = models.BooleanField(verbose_name="Listowanie użytkowników", default=False)
    Detail_user = models.BooleanField(verbose_name="Detale użytkownika", default=False)

    def __str__(self) -> str:
        return f"{self.User.username}'s permissions"
    



# class Adresy(models.Model):
#     AdresID = models.AutoField(primary_key=True)
#     Miasto =  models.CharField(max_length=50, null=False)
#     Kodpocztowy = models.CharField(max_length = 5,null = False)
#     Ulica =  models.CharField(max_length=50, null=False)
#     Nr_domu =  models.PositiveIntegerField( null=False)
#     Nr_mieszkania =  models.PositiveIntegerField( null=True)

