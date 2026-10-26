from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_view, name='register'),
    path('confirm-email/<uuid:token>/', confirm_email_view, name='confirm_email'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('change-password/', change_pass_view, name='change_pass'),
]
