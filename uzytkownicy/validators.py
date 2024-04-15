from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

#walidacja cyfry kontrolnej
def validate_pesel(value: str):
    control_number = 0
    weights = [1,3,7,9,1,3,7,9,1,3]
    i = 0
    for digit in value[:-1]:
        number_to_add = int(digit)*weights[i]
        control_number += number_to_add % 10
        i+=1
    output = 10 - (control_number % 10)

    if output != int(value[-1]):
        raise ValidationError("Niepoprawna liczba kontrolna w peselu")

#regex telefonu
regex_telefon = RegexValidator(regex=r'^\d{9}$', message="Niepoprawny numer telefonu")

#regex peselu
regex_pesel = RegexValidator(regex='^\d{11}$', message='PESEL musi mieć 11 znaków.')

#metoda zamieniajaca wybraną liczbe na podaną przez nas
def replace(input: str, index: int, number: str):
    list_input = list(input)
    list_input[index] = number
    return ''.join(list_input)