"""
URL configuration for biblioteka project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from uzytkownicy import views
from bibliotekarz import views as viewsb

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeSite.as_view(), name='home'),
    path('users/', views.ListUsersView.as_view(), name='users'),
    path('user/<int:pk>', views.DetailUserView.as_view(), name='user'),
    path('adduser/', views.AddUserView.as_view(), name='addUser'),
    path('updateuser/<int:pk>', views.UpdateUserView.as_view(), name='updateUser'),
    path('deleteuser/<int:pk>', views.DeleteUserView.as_view(), name='deleteUser'),
    path('permissions/<int:pk>', views.PermissionsView.as_view(), name='permissions'),
    path('password/<int:pk>', views.ChangeUserPasswordView.as_view(), name='password-change'),
    path('password/success', views.ChangeUserPasswordDoneView.as_view(), name='password-change-done'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('reset-password', views.ResetPasswordView.as_view(), name='reset-password'),
    path('list-permissions', views.ListPermissionsView.as_view(), name='list-permissions'),
    path('add-user-permission', views.AddUserPermissionView.as_view(), name='add-user-permission'),
    path('delete-user-permission', views.DeleteUserPermissionView.as_view(), name='delete-user-permission'),
    path('edit-user-permission', views.EditUserPermissionView.as_view(), name='edit-user-permission'),
    path('list-user-permission', views.ListUserPermissionView.as_view(), name='list-user-permission'),
    path('add-book-permission', views.AddBookPermissionView.as_view(), name='add-book-permission'),
    path('delete-book-permission', views.DeleteBookPermissionView.as_view(), name='delete-book-permission'),
    path('detail-user-permission', views.DetailUserPermissionView.as_view(), name='detail-user-permission'),
    path('edit-book-permission', views.EditBookPermissionView.as_view(), name='edit-book-permission'),
    path('detail-book-permission', views.DeleteBookPermissionView.as_view(), name='detail-book-permission'),
    path('register-book', viewsb.RegisterBookView.as_view(), name='register-book'),
    path('books', viewsb.ListBooksView.as_view(), name='books'),
    path('book/<int:pk>', viewsb.DetailBookView.as_view(), name='book'),
    path('borrow-book/<int:pk>', viewsb.BorrowBookView.as_view(), name='borrow-book'),
    path('rents', viewsb.ListRentsView.as_view(), name='rents'),
    path('registered-books', viewsb.RegisteredBooksView.as_view(), name='registered-books')
]
