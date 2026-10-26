from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from .maneger import *


class CostumUser(AbstractUser):
    username = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=200,unique=True)

    objects = CostumUserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class EmailConfirmation(models.Model):
    user = models.OneToOneField(CostumUser,on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4)




