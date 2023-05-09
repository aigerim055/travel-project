from django.core.mail import send_mail
from .models import UserProfile
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
# from celery import shared_task
 
format = '%d.%m.%Y'
 
# @shared_task(name='check_birthday')
def check_birthday():
    users = UserProfile.objects.all()
    for user in users:
        birthday = user.birthday.strptime(format)[:5]
        today = timezone.now().date().strptime(format)[:5]
        if birthday == today:
            html_message = render_to_string(
            'bio/birthday.html',
            )
            send_mail(
                'Поздравляем вас с днем рождения!',
                '',
                settings.EMAIL_HOST_USER,
                [user.user_profile.email],
                html_message=html_message,
                fail_silently=False   
        )