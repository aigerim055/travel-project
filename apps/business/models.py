from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify


User = get_user_model()


class BusinessProfile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='profile',
        unique=True
    )
    title = models.CharField(max_length=100, verbose_name='Название компании', unique=True)
    image = models.ImageField(upload_to='business_images')
    desc = models.CharField(max_length=200, verbose_name='О компании')
    phone = models.CharField(max_length=13, verbose_name='Номер телефона')
    email = models.EmailField(max_length=150, verbose_name='Электронная почта', blank=True)
    address = models.CharField(max_length=150, verbose_name='Адресс', blank=True)
    slug = models.SlugField(max_length=200, primary_key=True, blank=True)

    def save(self, *args, **kwargs):
        # if not self.slug:
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
   
    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Профиль компании'
        verbose_name_plural = 'Профили компаний'


class BusinessImage(models.Model):
    image = models.ImageField(upload_to='tour_images')
    business = models.ForeignKey(
        to=BusinessProfile,
        on_delete=models.CASCADE,
        related_name='bus_images'
    )


class Guide(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Юзер',
        related_name='guides',
    )
    company_name = models.ForeignKey(
        to=BusinessProfile,
        on_delete=models.CASCADE,
        verbose_name='Компания',
        related_name='comp',
        blank=True
    )
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    image = models.ImageField(upload_to='guides_images')
    age = models.PositiveSmallIntegerField()
    slug = models.SlugField(max_length=200, primary_key=True, blank=True)

    def save(self, *args, **kwargs):
        # if not self.slug:         
        self.slug = slugify(str(self.first_name + '-' + self.last_name))
        return super().save(*args, **kwargs)
    

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Гид'
        verbose_name_plural = 'Гиды'
