from django.urls import path
from .views import *


urlpatterns = [
    path('', home_view, name='home'),
    path('trips/', trip_list_view, name='trip_list'),
    path('trips/add/', trip_create_view, name='trip_create'),
    path('trips/<int:pk>/edit/', trip_edit_view, name='trip_edit'),
    path('trips/<int:pk>/delete/', trip_delete_view, name='trip_delete'),
    path('trips/<int:pk>/book/', book_trip_view, name='trip_book'),
    path('trips/<int:pk>/bookings/', trip_bookings_view, name='trip_bookings'),
    path('bookings/<int:pk>/<str:decision>/', decide_booking_view, name='booking_decide'),
    path('bookings/<int:pk>/cancel/', cancel_booking_view, name='booking_cancel'),
    path('requests/', request_list_view, name='request_list'),
    path('requests/add/', request_create_view, name='request_create'),
    path('requests/<int:pk>/edit/', request_edit_view, name='request_edit'),
    path('requests/<int:pk>/delete/', request_delete_view, name='request_delete'),
]
