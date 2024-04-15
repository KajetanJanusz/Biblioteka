from typing import Any
from django.db.models import Q
from django.core.paginator import Paginator
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from .models import User, Permissions
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import UserCreateUpdateForm, UserDeleteForm, UpdatePermissions
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


class HomeSite(ListView):
    model = User
    template_name = 'home.html'

class ListUsersView(ListView):
    model = User
    template_name = 'listUsers.html'
    
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


class DetailUserView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'detailUser.html'

class AddUserView(CreateView):
    model = User
    form_class = UserCreateUpdateForm
    template_name = 'addUser.html'
    success_url = reverse_lazy('users')

class UpdateUserView(UpdateView):
    model = User
    form_class = UserCreateUpdateForm
    template_name = 'updateUser.html'
    success_url = reverse_lazy('users')


class DeleteUserView(UpdateView):
    model = User
    form_class = UserDeleteForm
    template_name = 'deleteUser.html'
    success_url = reverse_lazy('users')

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
        except:
            messages.error(request, 'Użytkownik nie istnieje')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Zalogowano poprawnie.')
            return redirect('home')

    context = {'page': page}
    return render(request, 'login_register.html', context)


@login_required
def logoutPage(request):
    logout(request)
    return redirect('home')
