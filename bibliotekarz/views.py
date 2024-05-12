from django.db.models.query import QuerySet
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

class ListBooksView(ListView):
    model = Ksiazki
    template_name = 'listBooks.html'
    context_object_name = 'books'

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
        
class DetailBookView(DetailView):
    model = Ksiazki
    template_name = 'detailBook.html'
    context_object_name = 'book'

class RegisterBookView(CreateView):
    model = Ksiazki
    template_name = 'registerBook.html'
    form_class = RegisterBookForm
    success_url = reverse_lazy('home')

class BorrowBookView(FormView):
    model = Wypozyczenia
    template_name = 'borrowBook.html'
    form_class = RentBookForm
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        rent = Wypozyczenia(
        Data = datetime.now(),
        Data_zwrotu = datetime.now() + timedelta(30),
        KsiazkaID = Ksiazki.objects.get(id=self.kwargs['pk']),
        PracownikID = request.user,
        Stan = 0,
        KlientID = User.objects.get(id=self.request.POST.get('KlientID')))
        rent.save()
        book = Ksiazki.objects.get(id=rent.KsiazkaID.id)
        book.Liczba_egzamplarzy -= 1
        if book.Liczba_egzamplarzy == 0:
            book.Stan = 'Wypożyczona'
        book.save()
        return super().post(request, *args, **kwargs)

class ExtendReturnRentView(UpdateView):
    model = Wypozyczenia
    template_name = 'extendRental.html'
    success_url = reverse_lazy('rents')
    form_class = ExtendRentalForm

    def post(self, request, *args, **kwargs):
        rent = self.get_object()
        if 'extend' in request.POST:
            if rent.Stan in [1, 2, 3]:
                messages.error(request, 'Nie można przedłużyć tego wypożyczenia.')
                return redirect('rents')

            rent.Data_zwrotu = rent.Data_zwrotu + timedelta(30)
            rent.Stan = 1
            rent.save()
            messages.success(request, 'Wypożyczenie przedłużono pomyślnie')
            return redirect('rents')
        elif 'end' in request.POST:
            if rent.Stan == 3:
                messages.error(request, 'To wypożyczenie jest już zakończone')
                return redirect('rents')
            rent.Stan = 3
            rent.Data_zwrotu = datetime.now()
            book = Ksiazki.objects.get(id=rent.KsiazkaID.id)
            book.Liczba_egzamplarzy += 1
            if book.Liczba_egzamplarzy > 0:
                book.Stan = 'Dostępna'
            rent.save()
            book.save()
            messages.success(request, 'Wypożyczenie zakończono pomyślnie')
            return redirect('rents')

class ListRentsView(ListView):
    model = Permission
    template_name = 'rents.html'
    context_object_name = 'rents'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query != None:
            rents = Wypozyczenia.objects.filter(Q(KlientID__username__icontains=query) |
                                            Q(PracownikID__username__icontains=query) |
                                            Q(Stan__icontains=query))
            return rents
        else:
            rents = Wypozyczenia.objects.all()
            return rents

class RegisteredBooksView(ListView):
    model = Rejestracje
    template_name = 'booksRegistration.html'
    context_object_name = 'registrations'

    def get_queryset(self):
        query = self.request.GET.get('q')
        start = self.request.GET.get('start-date')
        end = self.request.GET.get('end-date')
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


