from typing import Any
from django.db.models import Q
from django.db.models.base import Model as Model
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from .models import User, Permissions
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, TemplateView, ListView, DetailView, CreateView, UpdateView, View
from .forms import UserCreateUpdateForm, UserDeleteForm, UpdatePermissions, UserChangePasswordForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from .methods import generate_password, send_email, change_passwords
from django.contrib.auth.views import LoginView


class HomeSite(ListView):
    model = User
    template_name = 'home.html'

class ListUsersView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'listUsers.html'

    def test_func(self) -> bool | None:
        return Permissions.objects.get(User=self.request.user.id).List_user
    
    def handle_no_permission(self):
        messages.info(self.request, 'Nie masz uprawnień, żeby wejść na tą stronę')
        return redirect('home')
    
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


class DetailUserView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'detailUser.html'

    def test_func(self) -> bool | None:
        return Permissions.objects.get(User=self.request.user.id).Detail_user
    
    def handle_no_permission(self):
        messages.info(self.request, 'Nie masz uprawnień, żeby wejść na tą stronę')
        return redirect('home')

class AddUserView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = UserCreateUpdateForm
    template_name = 'addUser.html'
    success_url = reverse_lazy('users')

    def test_func(self) -> bool | None:
        return Permissions.objects.get(User=self.request.user.id).Add_user
    
    def handle_no_permission(self):
        messages.info(self.request, 'Nie masz uprawnień, żeby wejść na tą stronę')
        return redirect('home')

class UpdateUserView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserCreateUpdateForm
    template_name = 'updateUser.html'
    success_url = reverse_lazy('users')

    def test_func(self) -> bool | None:
        return Permissions.objects.get(User=self.request.user.id).Edit_user
    
    def handle_no_permission(self):
        messages.info(self.request, 'Nie masz uprawnień, żeby wejść na tą stronę')
        return redirect('home')


class DeleteUserView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserDeleteForm
    template_name = 'deleteUser.html'
    success_url = reverse_lazy('users')

    def test_func(self) -> bool | None:
        return Permissions.objects.get(User=self.request.user.id).Delete_user
    
    def handle_no_permission(self):
        messages.info(self.request, 'Nie masz uprawnień, żeby wejść na tą stronę')
        return redirect('home')
    
class ChangeUserPasswordView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserChangePasswordForm
    template_name = 'updatePassword.html'
    success_url = reverse_lazy('users')

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        user = User.objects.get(id=self.kwargs['pk'])
        change_passwords(user)
        user.is_password_changed = False
        user.save()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.save()
        messages.success(self.request, 'Zaktualizowano!')
        return super().form_valid(form)

    def test_func(self) -> bool | None:
        if User.objects.get(id=self.kwargs['pk']) == self.request.user:
            return True
        else:
            return Permissions.objects.get(User=self.request.user.id).Edit_user
    
    def handle_no_permission(self):
        messages.info(self.request, 'Nie masz uprawnień, żeby wejść na tą stronę')
        return redirect('home')

class ChangeUserPasswordDoneView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'updatePasswordDone.html'
    uccess_url = reverse_lazy('home')

    def test_func(self) -> bool | None:
        if User.objects.get(id=self.kwargs['pk']) == self.request.user:
            return True
        else:
            return Permissions.objects.get(User=self.request.user.id).Edit_user
    
    def handle_no_permission(self):
        messages.info(self.request, 'Nie masz uprawnień, żeby wejść na tą stronę')
        return redirect('home')

class ResetPasswordView(FormView):
    form_class = UserChangePasswordForm
    template_name = 'resetPassword.html'

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.error(request, "Zły email lub login")
            return redirect('reset-password')
        
        if user.email != email:
            messages.error(request, 'Zły email lub login')
            return redirect('reset-password')
        
        new_password = generate_password()
        change_passwords(user)
        user.current_password = new_password
        user.is_password_changed = True
        user.save()
        send_email(new_password, user)
        messages.success(request, "Email z hasłem został wysłany")
        return redirect('login')
    
    def test_func(self) -> bool | None:
        if User.objects.get(id=self.kwargs['pk']) == self.request.user:
            return True
        else:
            return Permissions.objects.get(User=self.request.user.id).Edit_user
    
    def handle_no_permission(self):
        messages.info(self.request, 'Nie masz uprawnień, żeby wejść na tą stronę')
        return redirect('home')


class PermissionsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Permissions
    form_class = UpdatePermissions
    template_name = 'permissionsUser.html'
    success_url = reverse_lazy('users')

    def get_object(self):
        user = User.objects.get(id=self.kwargs['pk'])
        permission = Permissions.objects.get(User=user)

        return permission
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.save()
        messages.success(self.request, 'Zaktualizowano!')
        return super().form_valid(form)
    
    def test_func(self) -> bool | None:
        if User.objects.get(id=self.kwargs['pk']) == self.request.user:
            return True
        else:
            return Permissions.objects.get(User=self.request.user.id).Edit_user
    
    def handle_no_permission(self):
        messages.info(self.request, 'Nie masz uprawnień, żeby wejść na tą stronę')
        return redirect('home')


class CustomLoginView(LoginView):
    template_name = 'login_register.html'

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.error(request, "Niepoprawny login lub hasło")
            return redirect('login')
        
        if user.passwords_attempts >= 3:
            messages.error(request, 'Twoje konto jest zablokowane, napisz do administratora')
            return redirect('login')

        if user.current_password != password:
            user.passwords_attempts += 1
            user.save()
            messages.error(request, 'Nieprawidłowe hasło lub nazwa użytkownika')
            return redirect('login')

        if user.is_password_changed == True:
            messages.info(request, 'Hasło zostało wygenerowane. Zmień hasło')
            return redirect(reverse('password-change', kwargs={'pk': user.id}))
            

        login(self.request, user)
        messages.success(request, 'Zalogowano poprawnie.')
        return redirect('home')


class CustomLogoutView(LoginRequiredMixin, View):
    template_name = 'logout.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')

class ListPermissionsView(TemplateView):
    template_name = 'listPermissions.html'

class AddUserPermissionView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'listUsers.html'
    permission = Permissions.objects.filter(Add_user=True).values_list('User', flat=True)

    def get_queryset(self):
        users = User.objects.filter(id__in=self.permission)
        return users
    
    def test_func(self, *args, **kwargs) -> bool | None:
        return Permissions.objects.get(User=self.request.user.id).Edit_user
    
    def handle_no_permission(self):
        messages.info(self.request, 'Nie masz uprawnień, żeby wejść na tą stronę')
        return redirect('home')
    
class ListUserPermissionView(AddUserPermissionView):
    permission = Permissions.objects.filter(List_user=True).values_list('User', flat=True)

class DeleteUserPermissionView(AddUserPermissionView):
    permission = Permissions.objects.filter(Delete_user=True).values_list('User', flat=True)

class EditUserPermissionView(AddUserPermissionView):
    permission = Permissions.objects.filter(Edit_user=True).values_list('User', flat=True)

class DetailUserPermissionView(AddUserPermissionView):
    permission = Permissions.objects.filter(Edit_user=True).values_list('User', flat=True)

class AddBookPermissionView(AddUserPermissionView):
    permission = Permissions.objects.filter(Add_books=True).values_list('User', flat=True)

class DeleteBookPermissionView(AddUserPermissionView):
    permission = Permissions.objects.filter(Delete_books=True).values_list('User', flat=True)

class EditBookPermissionView(AddUserPermissionView):
    permission = Permissions.objects.filter(Edit_books=True).values_list('User', flat=True)

class DetailBookPermissionView(AddUserPermissionView):
    permission = Permissions.objects.filter(Detail_book=True).values_list('User', flat=True)



