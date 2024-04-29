from typing import Any
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from .models import User, Permissions
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, ListView, DetailView, CreateView, UpdateView
from .forms import UserCreateUpdateForm, UserDeleteForm, UpdatePermissions, UserChangePasswordForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.conf import settings
from django.core.mail import send_mail
from random import choice, randint
from string import ascii_lowercase, ascii_uppercase
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError


class HomeSite(ListView):
    model = User
    template_name = 'home.html'

class ListUsersView(UserPassesTestMixin, ListView):
    model = User
    template_name = 'listUsers.html'

    def test_func(self) -> bool | None:
        return Permissions.objects.get(User=self.request.user.id).List_user
    
    def handle_no_permission(self):
        return redirect('home')
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query != None:
            users = User.objects.filter(Q(first_name__icontains=query) |
                                            Q(last_name__icontains=query) |
                                            Q(username__icontains=query) |
                                            Q(user__permissions__icontaints=query),
                                            is_superuser=False, is_deleted=False).order_by('-utworzony')
            return users
        else:
            users = User.objects.filter(is_superuser=False,
                    is_deleted=False).order_by('-utworzony')
            return users


class DetailUserView(UserPassesTestMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'detailUser.html'

    def test_func(self) -> bool | None:
        return Permissions.objects.get(User=self.request.user.id).Detail_user
    
    def handle_no_permission(self):
        return redirect('home')

class AddUserView(UserPassesTestMixin, CreateView):
    model = User
    form_class = UserCreateUpdateForm
    template_name = 'addUser.html'
    success_url = reverse_lazy('users')

    def test_func(self) -> bool | None:
        return Permissions.objects.get(User=self.request.user.id).Add_user
    
    def handle_no_permission(self):
        return redirect('home')

class UpdateUserView(UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserCreateUpdateForm
    template_name = 'updateUser.html'
    success_url = reverse_lazy('users')

    def test_func(self) -> bool | None:
        return Permissions.objects.get(User=self.request.user.id).Edit_user
    
    def handle_no_permission(self):
        return redirect('home')


class DeleteUserView(UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserDeleteForm
    template_name = 'deleteUser.html'
    success_url = reverse_lazy('users')

    def test_func(self) -> bool | None:
        return Permissions.objects.get(User=self.request.user.id).Delete_user
    
    def handle_no_permission(self):
        return redirect('home')
    
class ChangeUserPasswordView(UpdateView):
    model = User
    form_class = UserChangePasswordForm
    template_name = 'updatePassword.html'
    success_url = reverse_lazy('password-change-done')

class ChangeUserPasswordDoneView(TemplateView):
    template_name = 'updatePasswordDone.html'
    uccess_url = reverse_lazy('home')

class ResetPasswordView(FormView):
    form_class = UserChangePasswordForm
    template_name = 'resetPassword.html'

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.error(request, "Zły mail")
            return redirect('reset-password')
        
        if user.username == username and user.email == email:
            uppercase = list()
            for x in range(9):
                uppercase.append(choice(ascii_uppercase))
            lowercase = choice(ascii_lowercase)
            digit = randint(0,9)
            special_char = choice('!@#$%')
            new_password = f"{''.join(uppercase)}{lowercase}{digit}{special_char*2}"
            user.password_db = new_password
            user.generated_password = new_password
            user.save()
            with get_connection(  
                host=settings.EMAIL_HOST, 
                port=settings.EMAIL_PORT,  
                username=settings.EMAIL_HOST_USER, 
                password=settings.EMAIL_HOST_PASSWORD, 
                use_tls=settings.EMAIL_USE_TLS  
            ) as connection:  
                subject = 'Nowe hasło' 
                email_from = settings.EMAIL_HOST_USER  
                recipient_list = [user.email,]  
                message = f'Twoje nowe hasło {new_password}' 
                EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()
        return 

def resetPassword(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            # messages.error(request, "Zły mail")
            return redirect('reset-password')
        
        if user.username == username and user.email == email:
            uppercase = list()
            for x in range(9):
                uppercase.append(choice(ascii_uppercase))
            lowercase = choice(ascii_lowercase)
            digit = randint(0,9)
            special_char = choice('!@#$%')
            new_password = f"{''.join(uppercase)}{lowercase}{digit}{special_char*2}"
            user.password_db = new_password
            user.generated_password = new_password
            user.save()
            with get_connection(  
                host=settings.EMAIL_HOST, 
                port=settings.EMAIL_PORT,  
                username=settings.EMAIL_HOST_USER, 
                password=settings.EMAIL_HOST_PASSWORD, 
                use_tls=settings.EMAIL_USE_TLS  
            ) as connection:  
                subject = 'Nowe hasło' 
                email_from = settings.EMAIL_HOST_USER  
                recipient_list = [user.email,]  
                message = f'Twoje nowe hasło {new_password}' 
                EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()
 
            return redirect('login')

    return render(request, 'resetPassword.html')


def permissions(request, pk):
    permission = Permissions.objects.get(User=User.objects.get(id=pk))
    form = UpdatePermissions(instance=permission)

    if request.method == "POST":
        form = UpdatePermissions(request.POST, instance=permission)
        if form.is_valid():
            form.save()
            return redirect('users')

    return render(request, 'permissionsUser.html', {'form': form})

def registerPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, form)
            return redirect('home')
        else:
            messages.error(request, 'Coś poszło nie tak :/')

    return render(request, 'login_register.html', {'form': form})


def loginPage(request):
    page = 'login'
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.error(request, "Niepoprawny login lub hasło")
            return redirect('login')
        
        if user.username == username and user.password_db != password:
            user.passwords_attempts = user.passwords_attempts + 1
            user.save()
            if user.passwords_attempts >= 3:
                messages.error(request, 'Twoje konto jest zablokowane, napisz do administratora')
                return redirect('login')
            else:
                messages.error(request, "Niepoprawny login lub hasło")
                return redirect('login')

        elif user.password_db == password and user.username == username:
            if user.passwords_attempts >= 3:
                messages.error(request, 'Twoje konto jest zablokowane, napisz do administratora')
                return redirect('login')
            if user.password_db == user.generated_password:
                login(request, user)
                return redirect('password-change', pk=user.id)
            
            login(request, user)
            messages.success(request, 'Zalogowano poprawnie.')
            return redirect('home')
        else:
            messages.error(request, "Niepoprawny login lub hasło")
            return redirect('login')


    context = {'page': page}
    return render(request, 'login_register.html', context)


@login_required
def logoutPage(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    
    return render(request, 'logout.html')

def listPermissions(request):
    return render(request, 'listPermissions.html')


def addUserPermission(request):
    permission = Permissions.objects.filter(Add_user=True)
    users = []
    for x in permission:
        users.append(User.objects.get(id=x.User.id))

    context = {'object_list':users}

    return render(request, 'listUsers.html', context=context)

def deleteUserPermission(request):
    permission = Permissions.objects.filter(Delete_user=True)
    users = []
    for x in permission:
        users.append(User.objects.get(id=x.User.id))

    context = {'object_list':users}

    return render(request, 'listUsers.html', context=context)

def editUserPermission(request):
    permission = Permissions.objects.filter(Edit_user=True)
    users = []
    for x in permission:
        users.append(User.objects.get(id=x.User.id))

    context = {'object_list':users}

    return render(request, 'listUsers.html', context=context)

def detailUserPermission(request):
    permission = Permissions.objects.filter(Detail_user=True)
    users = []
    for x in permission:
        users.append(User.objects.get(id=x.User.id))

    context = {'object_list':users}

    return render(request, 'listUsers.html', context=context)

def addBookPermission(request):
    permission = Permissions.objects.filter(Add_books=True)
    users = []
    for x in permission:
        users.append(User.objects.get(id=x.User.id))

    context = {'object_list':users}

    return render(request, 'listUsers.html', context=context)

def deleteBookPermission(request):
    permission = Permissions.objects.filter(Delete_books=True)
    users = []
    for x in permission:
        users.append(User.objects.get(id=x.User.id))

    context = {'object_list':users}

    return render(request, 'listUsers.html', context=context)

def editBookPermission(request):
    permission = Permissions.objects.filter(Edit_books=True)
    users = []
    for x in permission:
        users.append(User.objects.get(id=x.User.id))

    context = {'object_list':users}

    return render(request, 'listUsers.html', context=context)

def detailBookPermission(request):
    permission = Permissions.objects.filter(Detail_book=True)
    users = []
    for x in permission:
        users.append(User.objects.get(id=x.User.id))

    context = {'object_list':users}

    return render(request, 'listUsers.html', context=context)

def listUserPermission(request):
    permission = Permissions.objects.filter(List_user=True)
    users = []
    for x in permission:
        users.append(User.objects.get(id=x.User.id))

    context = {'object_list':users}

    return render(request, 'listUsers.html', context=context)

