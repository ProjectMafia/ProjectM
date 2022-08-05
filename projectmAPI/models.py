from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    login = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, default=-1)
    nick = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    country = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    photo = models.TextField()
