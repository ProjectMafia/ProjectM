from django.db import models


class BaseStructModel(models.Model):
    is_delete = models.BooleanField('Удалена ли запись', default=False)
    class Meta:
        abstract = True

class TimeStampMixin(models.Model):
    timestamp_create = models.DateTimeField('Время создания', auto_now_add=True)
    timestamp_update = models.DateTimeField('Время обновления', auto_now=True)

    class Meta:
        abstract = True


class AddressMixin(models.Model):
    country = models.CharField('Страна', max_length=40, blank=True)
    city = models.CharField('Город', max_length=40, blank=True)
    address = models.TextField('Адрес', blank=True)

    class Meta:
        abstract = True


class DescriptionMixin(models.Model):
    description = models.TextField('Описание', blank=True)

    class Meta:
        abstract = True