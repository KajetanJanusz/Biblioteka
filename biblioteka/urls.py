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
from django.urls import path
from uzytkownicy import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeSite.as_view(), name='home'),
    path('users/', views.ListUsersView.as_view(), name='users'),
    path('user/<int:pk>', views.DetailUserView.as_view(), name='user'),
    path('adduser/', views.AddUserView.as_view(), name='addUser'),
    path('updateuser/<int:pk>', views.UpdateUserView.as_view(), name='updateUser'),
    path('deleteuser/<int:pk>', views.DeleteUserView.as_view(), name='deleteUser'),
    path('permissions/<int:pk>', views.permissions, name='permissions'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
]
