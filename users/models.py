from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Класс - пользователи"""
    username = None
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='город', help_text='напишите город')
    phone = models.CharField(max_length=11, unique=True, verbose_name="Телефон", blank=True, null=True,
                             help_text='Введите номер телефона')
    email = models.EmailField(unique=True, verbose_name='Почта', help_text='Введите вашу почту')
    avatar = models.ImageField(upload_to='users/avatar', blank=True, null=True, verbose_name='Аватар',
                               help_text='Загрузите ваш аватар')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        """Метаданные"""
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """Строковый вывод"""
        return self.email
