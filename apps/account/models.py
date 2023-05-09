import code
from tabnanny import verbose
from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    
    def _create(self, username, phone, password, **extra_fields):
        if not username and phone:
            raise ValueError('User must have username and phone')
        user = self.model(
            username=username,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, phone, password, **extra_fields):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_staff', False)
        return self._create(username, phone, password, **extra_fields)

    def create_superuser(self, username, phone, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        return self._create(username, phone, password, **extra_fields)


class User(AbstractBaseUser):
    RANDOM_STRING_CHARS = "1234567890"

    CONFIRM_CHOICES = (
        ('email', 'E-MAIL'),
        ('phone', 'SMS')
    )

    username = models.CharField(max_length=50, primary_key=True, unique=True)
    phone = models.CharField(max_length=13, blank=True)  # , unique=True)
    email = models.CharField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=10, blank=True)
    code_method = models.CharField(choices=CONFIRM_CHOICES, max_length=6, default='email')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone', 'email']

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj=None):
        return self.is_staff

    def create_activation_code(self):
        code = get_random_string(length=6, allowed_chars=self.RANDOM_STRING_CHARS)
        if User.objects.filter(activation_code=code).exists():
            self.create_activation_code()
        self.activation_code = code
        self.save()

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'