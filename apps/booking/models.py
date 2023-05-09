from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from apps.tour.models import ConcreteTour

User = get_user_model()

class TourPurchase(models.Model):
    RANDOM_STRING_CHARS = "1234567890"

    STATUS_CHOICES = (
        ('pending', 'Ожидается'),
        ('finished', 'Пройден')
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.RESTRICT,
        related_name='orders'
    )
    tour = models.ManyToManyField(
        to=ConcreteTour,
        through='TourItems',
    )
    order_id = models.CharField(max_length=58, blank=True)
    total_sum = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=6, blank=True)

    def __str__(self):
        return f'Заказ № {self.order_id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.order_id:
            self.order_id = str(self.user.username) + '-' + (str(self.created_at))[9:16].replace(':', '-').replace(' ', '-')
        return self.order_id

    def create_code(self):
        code = get_random_string(length=6, allowed_chars=self.RANDOM_STRING_CHARS)
        if TourPurchase.objects.filter(code=code).exists():
            self.create_code()
        self.code = code
        self.save()

    class Meta:
        verbose_name = 'Покупка тура'
        verbose_name_plural = 'Покупки туров'


class TourItems(models.Model):
    order = models.ForeignKey(
        to=TourPurchase,
        on_delete=models.SET_NULL, 
        related_name='items',
        null=True
    )
    tour = models.ForeignKey(
        to=ConcreteTour,
        on_delete=models.SET_NULL,
        related_name='items',
        null=True
    )
    people_num = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Объект корзины'
        verbose_name_plural = 'Объекты корзины'