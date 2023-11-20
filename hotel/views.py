import logging
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Room
from .models import Reservation
from . import views
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


def login_view(request):
    if request.method == 'POST':
        staff_id = request.POST['staffId']
        password = request.POST['password']

        with transaction.atomic():
            user = authenticate(request, username=staff_id, password=password)

            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                return render(request, 'login.html', {'error_message': 'Invalid credentials'})

    return render(request, 'login.html')

def reservations_view(request):
    # Add your view logic here
    return render(request, 'reservations.html')

from django.shortcuts import render, redirect
from .forms import ReservationForm

def reservation_view(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., save it to a database)
            # Redirect to a thank you page or another appropriate page
            return redirect('thank_you')
    else:
        form = ReservationForm()

    return render(request, 'reservation.html', {'form': form})


def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)  # Use your form for reservations

        if form.is_valid():
            room_type = form.cleaned_data['room_type']
            check_in_date = form.cleaned_data['start_date']
            check_out_date = form.cleaned_data['end_date']
            guest_name = form.cleaned_data['guest_name']

            # Check room availability
            try:
                room = Room.objects.get(room_type=room_type, status='Available')
            except Room.DoesNotExist:
                return render(request, 'reservations.html', {'error_message': 'No rooms available of this type'})

            # Create a reservation
            guest = Guest.objects.get(name=guest_name)  # Adjust based on your Guest model
            reservation = Reservation(
                guest=guest,
                room=room,
                check_in=check_in_date,
                check_out=check_out_date,
                # Set other fields as needed
            )
            reservation.save()

            # Update room status
            room.status = 'Occupied'
            room.save()

            return redirect('success_page')  # Redirect to a success page

    else:
        form = ReservationForm()  # If you have a form for reservations

    return render(request, 'reservations.html', {'form': form})


def redirect_to_rooms(request):
    return redirect('rooms')

def redirect_to_homepage(request):
    return redirect('homepage')


def rooms_views(request):
    # Retrieve all room data
    room_list = Room.objects.all()
    selected_room = None

    if request.method == 'POST':
        room_number = request.POST.get('room_selection')
        if room_number:
            try:
                selected_room = Room.objects.get(room_number=room_number)
            except Room.DoesNotExist:
                selected_room = None

    return render(request, 'rooms.html', {'room_list': room_list, 'selected_room': selected_room})


@csrf_exempt
def update_room_status(request):
    if request.method == 'POST':
        # Get the selected room and status
        selected_room = request.POST.get('selected_room')  # Updated parameter name
        selected_status = request.POST.get('room_status')

        print(f"Updating room {selected_room} status to {selected_status}")

        try:
            # Retrieve the room from the database
            room = Room.objects.get(room_number=selected_room)
        except Room.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Room not found'})

        # Update the room's status
        room.status = selected_status
        room.save()

        print("Room status updated")  # Add this line to check if the update is performed

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})




def create_user_view(request):
    if request.method == 'POST':
        staff_id = request.POST['staffId']

        # Create a new user with staff ID as the username and "password" as the default password
        user = User.objects.create_user(username=staff_id, password="password")

        # Save the user object
        user.save()

        return redirect('login_view')
