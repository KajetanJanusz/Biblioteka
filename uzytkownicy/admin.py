from typing import Any
from django.contrib import admin
from .models import User, Permissions
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

# Register your models here.

class MyUserAdmin(UserAdmin):
    model = User
    readonly_fields = ['edytowany', 'utworzony']
    fieldsets = UserAdmin.fieldsets + (
        ('Dodatkowe', {'fields': ('Telefon',
            'Pesel', 'Data_urodzenia', 'current_password', 'password_1',
             'password_2', 'password_3', 'passwords_attempts' ,'Plec', 'Bibliotekarz', 'ManagerBiblioteki',
            'is_deleted', 'is_password_changed', 'utworzony', 'edytowany')}),
    )

admin.site.register(User, MyUserAdmin)
admin.site.register(Permissions)
