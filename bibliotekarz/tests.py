from django.test import TestCase
from .models import Ksiazki, Rejestracje
from uzytkownicy.models import User

class ModelTestCase(TestCase):
    def test_create_rejestracja_on_ksiazki_creation(self):
        ksiazka = Ksiazki.objects.create(Tytul="Testowa Książka", PracownikID=User.objects.get(id=11))
        rejestracja_count = Rejestracje.objects.filter(KsiazkaID=ksiazka).count()
        self.assertEqual(rejestracja_count, 1)