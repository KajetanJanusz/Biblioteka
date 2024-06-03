from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView, ListView, DetailView, CreateView, UpdateView, View
from .models import Ksiazki, Wypozyczenia, Rejestracje, User
from django.urls import reverse_lazy, reverse
from .forms import RegisterBookForm, RentBookForm, ExtendRentalForm
from django.db.models import Q
from django.contrib.auth.models import Permission
from datetime import timedelta, datetime
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404

class HandleNoPermission(UserPassesTestMixin):

    def handle_no_permission(self):
        messages.info(self.request, 'Nie masz uprawnień, żeby wejść na tą stronę')
        return redirect('home')

class ListBooksView(LoginRequiredMixin, HandleNoPermission, ListView):
    model = Ksiazki
    template_name = 'listBooks.html'
    context_object_name = 'books'

    def test_func(self) -> bool | None:
        user = User.objects.get(id=self.request.user.id)
        if user.ManagerBiblioteki == True or user.Bibliotekarz == True:
            return True
        else:
            return False

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query != None:
            books = Ksiazki.objects.filter(Q(Tytul__icontains=query) |
                                            Q(Autor__icontains=query) |
                                            Q(Gatunek__Nazwa__icontains=query) |
                                            Q(Wydawnictwo__icontains=query) |
                                            Q(Stan__icontains=query))
            return books
        else:
            books = Ksiazki.objects.all()
            return books
        
class DetailBookView(LoginRequiredMixin, HandleNoPermission, DetailView):
    model = Ksiazki
    template_name = 'detailBook.html'
    context_object_name = 'book'

    def test_func(self) -> bool | None:
        return User.objects.get(id=self.request.user.id).Bibliotekarz

class RegisterBookView(LoginRequiredMixin, HandleNoPermission, CreateView):
    template_name = 'registerBook.html'
    form_class = RegisterBookForm
    success_url = reverse_lazy('home')

    def test_func(self) -> bool | None:
        return User.objects.get(id=self.request.user.id).Bibliotekarz

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        obj = form.save(commit=False)
        obj.Utworzone_przez = self.request.user
        obj.save()
        messages.success(self.request, 'Dodano książkę')
        return redirect('home')

class BorrowBookView(HandleNoPermission, FormView):
    model = Wypozyczenia
    template_name = 'borrowBook.html'
    form_class = RentBookForm
    success_url = reverse_lazy('home')

    def test_func(self) -> bool | None:
        return User.objects.get(id=self.request.user.id).Bibliotekarz

    def post(self, request, *args, **kwargs):
        return_date = self.request.POST.get('Data_zwrotu')
        rent = Wypozyczenia(
        Data = datetime.now(),
        Data_zwrotu = return_date if return_date else datetime.now() + timedelta(14),
        KsiazkaID = get_object_or_404(Ksiazki, id=self.kwargs['pk']),
        PracownikID = request.user,
        Stan = 'Nowe',
        KlientID = User.objects.get(id=self.request.POST.get('KlientID')))

        rent.save()
        
        book = get_object_or_404(Ksiazki, id=self.kwargs['pk'])
        book.Liczba_dostepnych_egzemplarzy = book.Liczba_dostepnych_egzemplarzy - 1
        if book.Liczba_dostepnych_egzemplarzy <= 0:
            book.Stan = 'Wypożyczona'

        book.save()

        messages.success(request, 'Książka została wypożyczona')
        
        return redirect('home')

class ExtendReturnRentView(HandleNoPermission, UpdateView):
    model = Wypozyczenia
    template_name = 'extendRental.html'
    success_url = reverse_lazy('rents')
    form_class = ExtendRentalForm

    def test_func(self) -> bool | None:
        return User.objects.get(id=self.request.user.id).Bibliotekarz

    def post(self, request, *args, **kwargs):
        rent = self.get_object()
        if 'extend' in request.POST:
            if rent.Stan in ['Po terminie', 'Zakończone']:
                messages.error(request, 'Nie można przedłużyć tego wypożyczenia.')
                return redirect('rents')

            rent.Data_zwrotu = rent.Data_zwrotu + timedelta(14)
            rent.Stan = 'Przedłużone'
            rent.save()
            messages.success(request, 'Wypożyczenie przedłużono pomyślnie')
            return redirect('rents')
        elif 'end' in request.POST:
            if rent.Stan == 'Zakończone':
                messages.error(request, 'To wypożyczenie jest już zakończone')
                return redirect('rents')
            rent.Stan = 'Zakończone'
            rent.Data_zwrotu = datetime.now()
            book = Ksiazki.objects.get(id=rent.KsiazkaID.id)
            book.Liczba_dostepnych_egzemplarzy += 1
            if book.Liczba_dostepnych_egzemplarzy > 0:
                book.Stan = 'Dostępna'
            rent.save()
            book.save()
            messages.success(request, 'Wypożyczenie zakończono pomyślnie')
            return redirect('rents')

class ListRentsView(HandleNoPermission, ListView):
    model = Wypozyczenia
    template_name = 'rents.html'
    context_object_name = 'rents'

    def test_func(self) -> bool | None:
        user = User.objects.get(id=self.request.user.id)
        if user.Bibliotekarz == True:
            return True
        elif user.ManagerBiblioteki == True:
            return True
        else:
            return False

    def get_queryset(self):
        query = self.request.GET.get('q')
        start = self.request.GET.get('start-date')
        end = self.request.GET.get('end-date')
        if query:
            rents = Wypozyczenia.objects.filter(Q(KlientID__username__icontains=query) |
                                            Q(PracownikID__username__icontains=query) |
                                            Q(Stan__icontains=query))
            return rents
        elif start and end:
            rents = Wypozyczenia.objects.filter(Data_zwrotu__gte=start, Data_zwrotu__lte=end)
            return rents
        else:
            rents = Wypozyczenia.objects.all()
            return rents

class RegisteredBooksView(LoginRequiredMixin, HandleNoPermission, ListView):
    model = Rejestracje
    template_name = 'booksRegistration.html'
    context_object_name = 'registrations'

    def test_func(self) -> bool | None:
        return User.objects.get(id=self.request.user.id).ManagerBiblioteki

    def get_queryset(self):
        query = self.request.GET.get('q')
        start = self.request.GET.get('start-date')
        end = self.request.GET.get('end-date')

        print(start, end)
        if query:
            registrations = Rejestracje.objects.filter(Q(KsiazkaID__Tytul__icontains=query) |
                                                       Q(KsiazkaID__Autor__icontains=query) |
                                                       Q(KsiazkaID__Gatunek__Nazwa__icontains=query) |
                                                       Q(KsiazkaID__Wydawnictwo__icontains=query) |
                                                       Q(PracownikID__username__icontains=query))
            return registrations
        elif start and end:
            registrations = Rejestracje.objects.filter(Data__gte=start, Data__lte=end)
            return registrations
        else:
            registrations = Rejestracje.objects.all()
            return registrations


