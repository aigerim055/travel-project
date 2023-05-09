from django.conf import settings
# from config.celery import app
from django.core.mail import send_mail
from django.template.loader import render_to_string


# @app.task
def send_details(email, code):
    html_message = render_to_string(
        'booking/confirmation_mail.html',
        {'confirmation_code': code}
        )
        
    send_mail(
        'Детали вашего тура',
        '',
        settings.EMAIL_HOST_USER,
        [email],
        html_message=html_message,
        fail_silently=False   
    )