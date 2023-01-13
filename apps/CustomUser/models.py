from django.db import models
from apps.projectmAPI.modelmixins import *
from django.contrib.auth.models import AbstractUser
#from .managers import *


class UserM(AbstractUser, BaseStructModel, AddressMixin, DescriptionMixin):
    nickname = models.CharField('Игровой ник', max_length=50, unique=True)
    #objects = UserMManager
    REQUIRED_FIELDS = ['nickname']
    def __str__(self) -> str:
        return f'{self.nickname}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


