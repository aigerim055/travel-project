from django.db import models
from slugify import slugify

from django.contrib.auth import get_user_model

from apps.business.models import BusinessProfile, Guide
from datetime import datetime

current = str(datetime.now())


User = get_user_model()

class Tour(models.Model):

    LEVEL_CHOICES = (
        ('easy', 'легкий'),
        ('medium', 'средний'),
        ('hard', 'сложный')
    )

    title = models.CharField(max_length=100, verbose_name='Название тура')
    slug = models.SlugField(max_length=120, primary_key=True, blank=True)

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Юзер',
        related_name='tours',
    )
    company_name = models.ForeignKey(
        to=BusinessProfile,
        on_delete=models.CASCADE,
        verbose_name='Компания',
        related_name='company'
    )
    image = models.ImageField(upload_to='media/tour_image', blank=True)
    place = models.CharField(max_length=100, verbose_name='Место')
    desc = models.CharField(max_length=150)
    number_of_days = models.PositiveIntegerField()
    level = models.CharField(max_length=8, choices=LEVEL_CHOICES, verbose_name='Уровень')

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'


class ConcreteTour(models.Model):

    tour = models.ForeignKey(
        to=Tour,
        on_delete=models.CASCADE,
        verbose_name='Тур',
        related_name='concrete_tour'
    )
    guide = models.ForeignKey(
        to=Guide,
        on_delete=models.CASCADE,
        verbose_name='Гид',
        related_name='tour'
    )
    slug = models.SlugField(max_length=120, primary_key=True, blank=True)
    price_som = models.PositiveSmallIntegerField(verbose_name='Цена в национальной валюте')
    price_usd = models.PositiveSmallIntegerField(verbose_name='Цена в USD', blank=True)
    date = models.DateField()
    people_count = models.PositiveSmallIntegerField(verbose_name='Количество мест на тур')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.tour.title) + '-' + current[11:19].replace(':', '')) 
        if not self.price_usd:
            self.price_usd = round(self.price_som / 84, 1)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Конкретный тур'
        verbose_name_plural = 'Конкретные туры'

    def __str__(self) -> str:
        return f'Тур в {self.tour.title} {self.date}'


class TourImage(models.Model):
    image = models.ImageField(upload_to='media/tour_image')
    tour = models.ForeignKey(
        to=Tour,
        on_delete=models.CASCADE,
        related_name='tour_images',
    )
