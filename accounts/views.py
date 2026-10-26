from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import *
from .helper import *
from .models import *


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password1', '')
        confirm_password = request.POST.get('password2', '')

        if not username or not email:
            return render(request, 'register.html', {'error': 'Заполните имя и адрес электронной почты.'})
        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Пароли не совпадают.'})
        if CostumUser.objects.filter(email__iexact=email).exists():
            return render(request, 'register.html', {'error': 'Этот адрес электронной почты уже зарегистрирован.'})

        user = CostumUser.objects.create_user(email=email, username=username, password=password)
        token = EmailConfirmation.objects.create(user=user)
        send_confirmed_token(token)
        return render(request, 'register.html', {'success': 'Ссылка для подтверждения отправлена на вашу почту.'})

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password1', '')
        user = authenticate(request, email=email, password=password)
        if user is None:
            return render(request, 'login.html', {'error': 'Неверный адрес электронной почты или пароль.'})
        login(request, user)
        return redirect('home')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def confirm_email_view(request, token):
    confirmation = get_object_or_404(EmailConfirmation, token=token)
    user = confirmation.user
    user.is_active = True
    user.save(update_fields=['is_active'])
    confirmation.delete()
    return render(request, 'login.html', {'success': 'Электронная почта подтверждена. Теперь войдите в аккаунт.'})


@login_required
def change_pass_view(request):
    error = ''
    if request.method == 'POST':
        old_password = request.POST.get('old_pass', '')
        new_password = request.POST.get('new_pass', '')
        confirm_password = request.POST.get('conf_pass', '')
        if not request.user.check_password(old_password):
            error = 'Текущий пароль указан неверно.'
        elif new_password != confirm_password:
            error = 'Новые пароли не совпадают.'
        elif len(new_password) < 8:
            error = 'Пароль должен содержать не менее 8 символов.'
        else:
            request.user.set_password(new_password)
            request.user.save()
            return redirect('login')
    return render(request, 'change_pass.html', {'error': error})