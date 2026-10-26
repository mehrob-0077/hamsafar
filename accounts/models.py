from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from .maneger import *


class CostumUser(AbstractUser):
    username = models.CharField('Имя', max_length=150, blank=True)
    email = models.EmailField('Электронная почта', max_length=200, unique=True)

    objects = CostumUserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class EmailConfirmation(models.Model):
    user = models.OneToOneField(CostumUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    token = models.UUIDField('Токен подтверждения', default=uuid.uuid4)

    class Meta:
        verbose_name = 'Подтверждение электронной почты'
        verbose_name_plural = 'Подтверждения электронной почты'




