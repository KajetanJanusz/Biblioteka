from random import choice, randint
from string import ascii_lowercase, ascii_uppercase
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from .models import User

def generate_password():
    uppercase = list()
    for x in range(9):
        uppercase.append(choice(ascii_uppercase))
    lowercase = choice(ascii_lowercase)
    digit = randint(0,9)
    special_char = choice('!@#$%')
    new_password = f"{''.join(uppercase)}{lowercase}{digit}{special_char*2}"
    return new_password

def send_email(new_password, user):
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

def change_passwords(user: User):
    user.password_3 = user.password_2
    user.password_2 = user.password_1
    user.password_1 = user.current_password


    