from django.contrib import admin
from .models import Trip, CompanionRequest, TripBooking


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('start_location', 'end_location', 'date', 'seats_available', 'user')
    list_filter = ('date',)
    search_fields = ('start_location', 'end_location', 'user__email')


@admin.register(CompanionRequest)
class CompanionRequestAdmin(admin.ModelAdmin):
    list_display = ('start_location', 'end_location', 'date', 'user')
    list_filter = ('date',)
    search_fields = ('start_location', 'end_location', 'user__email')


@admin.register(TripBooking)
class TripBookingAdmin(admin.ModelAdmin):
    list_display = ('trip', 'passenger_name', 'gender', 'seats_count', 'status', 'created_at')
    list_filter = ('status', 'created_at')
