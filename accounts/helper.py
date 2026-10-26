from django.core.mail import send_mail
from django.conf import settings


def send_confirmed_token(token):
    send_mail(
        subject="Добро пожаловать в HamSafar",
        message=f"Подтвердите аккаунт: {settings.SITE_URL}/confirm-email/{token.token}/",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list =  [token.user.email],
    )

