from django import forms
from .models import Trip, CompanionRequest, TripBooking


class TripForm(forms.ModelForm):
    date = forms.DateTimeField(
        label='Дата и время',
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M',
        ),
    )

    class Meta:
        model = Trip
        fields = ('start_location', 'end_location', 'date', 'seats_available', 'description')


class CompanionRequestForm(forms.ModelForm):
    date = forms.DateTimeField(
        label='Дата и время',
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M',
        ),
    )

    class Meta:
        model = CompanionRequest
        fields = ('start_location', 'end_location', 'date', 'description')


class BookingForm(forms.Form):
    passenger_name = forms.CharField(label='Имя', max_length=100)
    gender = forms.ChoiceField(
        label='Пол',
        choices=[('', 'Выберите'), *TripBooking.GENDER_CHOICES],
    )
    seats_count = forms.IntegerField(label='Количество мест', min_value=1)

    def __init__(self, data=None, max_seats=1):
        super().__init__(data)
        self.fields['seats_count'].max_value = max_seats
