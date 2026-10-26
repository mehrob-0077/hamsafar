from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('trips/', views.trip_list_view, name='trip_list'),
    path('trips/add/', views.trip_create_view, name='trip_create'),
    path('trips/<int:pk>/edit/', views.trip_edit_view, name='trip_edit'),
    path('trips/<int:pk>/delete/', views.trip_delete_view, name='trip_delete'),
    path('trips/<int:pk>/book/', views.book_trip_view, name='trip_book'),
    path('trips/<int:pk>/bookings/', views.trip_bookings_view, name='trip_bookings'),
    path('bookings/<int:pk>/<str:decision>/', views.decide_booking_view, name='booking_decide'),
    path('bookings/<int:pk>/cancel/', views.cancel_booking_view, name='booking_cancel'),
    path('requests/', views.request_list_view, name='request_list'),
    path('requests/add/', views.request_create_view, name='request_create'),
    path('requests/<int:pk>/edit/', views.request_edit_view, name='request_edit'),
    path('requests/<int:pk>/delete/', views.request_delete_view, name='request_delete'),
]
