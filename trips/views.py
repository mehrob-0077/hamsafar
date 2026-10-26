from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import BookingForm, CompanionRequestForm, TripForm
from .models import CompanionRequest, Trip, TripBooking


def home_view(request):
    trips = Trip.objects.filter(date__gte=timezone.now(), seats_available__gt=0)[:4]
    requests = CompanionRequest.objects.filter(date__gte=timezone.now())[:4]
    return render(request, 'home.html', {'trips': trips, 'requests': requests})


def trip_list_view(request):
    trips = Trip.objects.filter(date__gte=timezone.now())

    if request.user.is_authenticated:
        bookings = TripBooking.objects.filter(passenger=request.user)
        trips = trips.filter(
            Q(seats_available__gt=0) |
            Q(user=request.user) |
            Q(pk__in=bookings.values('trip_id'))
        )
        my_bookings = {booking.trip_id: booking for booking in bookings}
    else:
        trips = trips.filter(seats_available__gt=0)
        my_bookings = {}

    start = request.GET.get('start', '').strip()
    end = request.GET.get('end', '').strip()
    date = request.GET.get('date', '').strip()

    if start:
        trips = trips.filter(start_location__icontains=start)
    if end:
        trips = trips.filter(end_location__icontains=end)
    if date:
        trips = trips.filter(date__date=date)

    for trip in trips:
        trip.my_booking = my_bookings.get(trip.pk)

    return render(request, 'trip_list.html', {
        'trips': trips,
        'start': start,
        'end': end,
        'date': date,
    })


@login_required
def trip_create_view(request):
    form = TripForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        trip = form.save(commit=False)
        trip.user = request.user
        trip.save()
        return redirect('trip_list')

    return render(request, 'form.html', {
        'form': form,
        'title': 'Добавить поездку',
        'back_url': 'trip_list',
    })


@login_required
def trip_edit_view(request, pk):
    trip = get_object_or_404(Trip, pk=pk, user=request.user)
    form = TripForm(request.POST or None, instance=trip)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('trip_list')

    return render(request, 'form.html', {
        'form': form,
        'title': 'Редактировать поездку',
        'back_url': 'trip_list',
    })


@login_required
def trip_delete_view(request, pk):
    trip = get_object_or_404(Trip, pk=pk, user=request.user)

    if request.method == 'POST':
        trip.delete()
        return redirect('trip_list')

    return render(request, 'confirm_delete.html', {
        'object': trip,
        'kind': 'trip',
        'back_url': 'trip_list',
    })


@login_required
def book_trip_view(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    form = BookingForm(request.POST or None, max_seats=trip.seats_available)

    if trip.user == request.user or trip.date <= timezone.now():
        form.add_error(None, 'Нельзя отправить заявку на эту поездку.')
    elif TripBooking.objects.filter(trip=trip, passenger=request.user).exists():
        form.add_error(None, 'Вы уже отправили заявку на эту поездку.')
    elif request.method == 'POST' and form.is_valid():
        TripBooking.objects.create(
            trip=trip,
            passenger=request.user,
            passenger_name=form.cleaned_data['passenger_name'],
            gender=form.cleaned_data['gender'],
            seats_count=form.cleaned_data['seats_count'],
        )
        return redirect('trip_list')

    return render(request, 'form.html', {
        'form': form,
        'title': f'Заявка на поездку: {trip.start_location} — {trip.end_location}',
        'back_url': 'trip_list',
    })


@login_required
@require_POST
def cancel_booking_view(request, pk):
    booking = get_object_or_404(TripBooking, pk=pk, passenger=request.user)
    trip = booking.trip

    if booking.status == 'accepted' and trip.date > timezone.now():
        trip.seats_available += booking.seats_count
        trip.save(update_fields=['seats_available'])

    booking.delete()
    return redirect('trip_list')


@login_required
def trip_bookings_view(request, pk):
    trip = get_object_or_404(Trip, pk=pk, user=request.user)
    bookings = trip.bookings.select_related('passenger')
    return render(request, 'trip_bookings.html', {
        'trip': trip,
        'bookings': bookings,
    })


@login_required
@require_POST
def decide_booking_view(request, pk, decision):
    booking = get_object_or_404(
        TripBooking,
        pk=pk,
        trip__user=request.user,
    )

    if decision not in ('accept', 'reject'):
        return redirect('trip_bookings', pk=booking.trip_id)

    if booking.status == 'pending':
        if decision == 'accept' and booking.seats_count <= booking.trip.seats_available:
            booking.status = 'accepted'
            booking.trip.seats_available -= booking.seats_count
            booking.trip.save(update_fields=['seats_available'])
            booking.save(update_fields=['status'])
        elif decision == 'reject':
            booking.status = 'rejected'
            booking.save(update_fields=['status'])

    return redirect('trip_bookings', pk=booking.trip_id)


def request_list_view(request):
    requests = CompanionRequest.objects.filter(date__gte=timezone.now())
    start = request.GET.get('start', '').strip()
    end = request.GET.get('end', '').strip()
    date = request.GET.get('date', '').strip()

    if start:
        requests = requests.filter(start_location__icontains=start)
    if end:
        requests = requests.filter(end_location__icontains=end)
    if date:
        requests = requests.filter(date__date=date)

    return render(request, 'request_list.html', {
        'requests': requests,
        'start': start,
        'end': end,
        'date': date,
    })


@login_required
def request_create_view(request):
    form = CompanionRequestForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        return redirect('request_list')

    return render(request, 'form.html', {
        'form': form,
        'title': 'Заявка на поиск попутчика',
        'back_url': 'request_list',
    })


@login_required
def request_edit_view(request, pk):
    item = get_object_or_404(CompanionRequest, pk=pk, user=request.user)
    form = CompanionRequestForm(request.POST or None, instance=item)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('request_list')

    return render(request, 'form.html', {
        'form': form,
        'title': 'Изменить заявку',
        'back_url': 'request_list',
    })


@login_required
def request_delete_view(request, pk):
    item = get_object_or_404(CompanionRequest, pk=pk, user=request.user)

    if request.method == 'POST':
        item.delete()
        return redirect('request_list')

    return render(request, 'confirm_delete.html', {
        'object': item,
        'kind': 'request',
        'back_url': 'request_list',
    })
