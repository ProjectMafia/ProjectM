from django.contrib.auth.base_user import BaseUserManager
import random

class UserMManager(BaseUserManager):

    def create_user(self, username, password, *args, **kwargs):
        print(kwargs, args)
        if not password:
            for _ in range(12):
                password += random.choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ%?/.,@#$&*'))
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self, username, nickname, password, **kwargs):
        """
        Create and save a SuperUser with the given email and password.
        """
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        if kwargs.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if kwargs.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, nickname, password, **kwargs)