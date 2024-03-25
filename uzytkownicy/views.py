from typing import Any
from django.db.models import Q
from django.core.paginator import Paginator
from .models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import UserCreateUpdateForm, UserDeleteForm



class HomeSite(ListView):
    model = User
    template_name = 'home.html'

#wylistowanie użytkowników
class ListUsersView(ListView):
    model = User
    template_name = 'listUsers.html'
    
    #wyszukiwanie użytkowników po imieniu, nazwisku lub loginie
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query != None:
            users = User.objects.filter(Q(first_name__icontains=query) |
                                            Q(last_name__icontains=query) |
                                            Q(username__icontains=query),
                                            is_superuser=False, is_deleted=False).order_by('-utworzony')
            return users
        else:
            users = User.objects.filter(is_superuser=False,
                    is_deleted=False).order_by('-utworzony')
            return users


#szczegółowy widok użytkownika
class DetailUserView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'detailUser.html'

#utworzenie użytkownika
class AddUserView(CreateView):
    model = User
    form_class = UserCreateUpdateForm
    template_name = 'addUser.html'
    success_url = reverse_lazy('users')

#edycja użytkownika
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