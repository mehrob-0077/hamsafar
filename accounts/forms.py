from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from .models import CostumUser


class CostumUserCreateForms(UserCreationForm):
    class Meta:
        model = CostumUser
        fields = ('username', 'email')
        labels = {'username': 'Имя', 'email': 'Электронная почта'}


class CostumUserChangeForms(UserChangeForm):
    class Meta:
        model = CostumUser
        fields = ('username', 'email')
        labels = {'username': 'Имя', 'email': 'Электронная почта'}



