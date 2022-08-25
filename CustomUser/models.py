from django.db import models
from django.contrib.auth.models import AbstractUser

class UserM(AbstractUser):
    nickname = models.CharField('Ник', max_length=50, unique=True)

    timestamp_create = models.DateTimeField('Время создания', auto_now_add=True)
    timestamp_update = models.DateTimeField('Время обновления', auto_now=True)

    country = models.CharField('Страна', max_length=40)
    city = models.CharField('Город', max_length=40)
    address = models.TextField('Адрес')

    description = models.TextField('Описание')

    
    def __str__(self) -> str:
        return f'{self.nickname}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


