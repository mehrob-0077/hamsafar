from django.conf import settings
from django.db import models


class Trip(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trips', verbose_name='Пользователь')
    start_location = models.CharField('Откуда', max_length=150)
    end_location = models.CharField('Куда', max_length=150)
    date = models.DateTimeField('Дата и время')
    seats_available = models.PositiveIntegerField('Свободные места')
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        db_table = 'accounts_trip'
        ordering = ['date']
        verbose_name = 'Поездка'
        verbose_name_plural = 'Поездки'

    def __str__(self):
        return f'{self.start_location} - {self.end_location}'


class CompanionRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='companion_requests', verbose_name='Пользователь')
    start_location = models.CharField('Откуда', max_length=150)
    end_location = models.CharField('Куда', max_length=150)
    date = models.DateTimeField('Дата и время')
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        db_table = 'accounts_companionrequest'
        ordering = ['date']
        verbose_name = 'Заявка на поиск попутчика'
        verbose_name_plural = 'Заявки на поиск попутчика'

    def __str__(self):
        return f'{self.start_location} - {self.end_location}'


class TripBooking(models.Model):
    GENDER_CHOICES = [
        ('Мард', 'Мужчина'),
        ('Зан', 'Женщина'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='bookings', verbose_name='Поездка')
    passenger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trip_bookings', verbose_name='Пассажир')
    passenger_name = models.CharField('Имя пассажира', max_length=100, default='')
    gender = models.CharField('Пол', max_length=20, choices=GENDER_CHOICES, default='')
    seats_count = models.PositiveSmallIntegerField('Количество мест', default=1)
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['trip', 'passenger'], name='one_booking_per_passenger_trip'),
        ]
        ordering = ['created_at']
        verbose_name = 'Бронирование поездки'
        verbose_name_plural = 'Бронирования поездок'

    def __str__(self):
        return f'{self.passenger} - {self.trip}'
