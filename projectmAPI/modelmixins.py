from django.db import models


class BaseStructModel(models.Model):

    class Meta:
        abstract = True

class TimeStampMixin:
    timestamp_create = models.DateTimeField('Время создания', auto_now_add=True)
    timestamp_update = models.DateTimeField('Время обновления', auto_now=True)

    class Meta:
        abstract = True


class AddressMixin:
    country = models.CharField('Страна', max_length=40)
    city = models.CharField('Город', max_length=40)
    address = models.TextField('Адрес')

    class Meta:
        abstract = True


class DescriptionMixin:
    description = models.TextField('Описание')

    class Meta:
        abstract = True