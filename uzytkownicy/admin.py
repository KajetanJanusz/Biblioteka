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
            'Pesel', 'Data_urodzenia', 'password_db', 'generated_password', 'passwords_attempts' ,'Plec', 'pracownik',
            'is_deleted', 'utworzony', 'edytowany')}),
    )

admin.site.register(User, MyUserAdmin)
admin.site.register(Permissions)
