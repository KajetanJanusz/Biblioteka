from django.contrib import admin
from .models import Ksiazki, Wypozyczenia, Gatunki, Rejestracje
from django.contrib.auth.models import Permission

# Register your models here.

admin.site.register(Ksiazki)
admin.site.register(Wypozyczenia)
admin.site.register(Gatunki)
admin.site.register(Rejestracje)