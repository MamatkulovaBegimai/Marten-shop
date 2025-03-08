from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(verbose_name="Имя пользователя", max_length=100, unique=True)
    password = models.CharField(verbose_name="Пароль", max_length=50, unique=True)
    email = models.EmailField(verbose_name="Почта")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
