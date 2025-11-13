from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, login, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(login=login, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(login, email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    # Валидаторы
    cyrillic_validator = RegexValidator(
        regex=r'^[А-Яа-яЁё\s\-]+$',
        message='Разрешены только кириллица, пробел и тире'
    )
    
    latin_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9\-]+$',
        message='Разрешены только латиница, цифры и тире'
    )
    
    # Обязательные поля
    name = models.CharField(
        'Имя',
        max_length=100,
        validators=[cyrillic_validator]
    )
    
    surname = models.CharField(
        'Фамилия',
        max_length=100,
        validators=[cyrillic_validator]
    )
    
    patronymic = models.CharField(
        'Отчество',
        max_length=100,
        blank=True,
        null=True,
        validators=[cyrillic_validator]
    )
    
    login = models.CharField(
        'Логин',
        max_length=50,
        unique=True,
        validators=[latin_validator]
    )
    
    email = models.EmailField(
        'Email',
        unique=True
    )
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', 'name', 'surname']
    
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f'{self.surname} {self.name} ({self.login})'
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return self.is_superuser
