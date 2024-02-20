import logging
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Room
from .models import Reservation
from . import views
from .models import Guest
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def check_user_is_staff(sender, request, user, **kwargs):
    # Check if the user is staff
    if user.is_authenticated and user.is_staff:
        request.session['is_staff'] = True
    else:
        request.session['is_staff'] = False

@csrf_protect
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
            return redirect('reservation.html')
    else:
        form = ReservationForm()

    return render(request, 'reservation.html', {'form': form})

def generate_unique_user_id():
    while True:
        user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not Guest.objects.filter(user_id=user_id).exists():
            return user_id

def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)

        if form.is_valid():
            # Extract form data
            room_type = form.cleaned_data['room_type']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            guest_first_name = form.cleaned_data['guest_first_name']
            guest_last_name = form.cleaned_data['guest_last_name']
            guest_email = form.cleaned_data['guest_email']
            country_code = form.cleaned_data['country_code']
            guest_phone = form.cleaned_data['guest_phone']
            guest_address = form.cleaned_data['guest_address']

            # Use a transaction to ensure atomicity
            with transaction.atomic():
                # Check room availability
                try:
                    room = Room.objects.select_for_update().get(room_type=room_type, status='Available')
                except Room.DoesNotExist:
                    return render(request, 'reservations.html', {'error_message': 'No rooms available of this type'})

                # Check if the guest with the given email already exists
                try:
                    guest = Guest.objects.get(email=guest_email)
                except Guest.DoesNotExist:
                    # Guest does not exist, create a new one
                    guest = Guest.objects.create(
                        email=guest_email,
                        first_name=guest_first_name,
                        last_name=guest_last_name,
                        country_code=country_code,
                        phone=guest_phone,
                        address=guest_address,
                    )
                    # Generate a unique user ID
                    guest.user_id = generate_unique_user_id()
                    guest.save()

                # Assign the room to the guest
                room.guest_id = guest
                room.save()

                # Create a reservation
                reservation = Reservation.objects.create(
                    guest=guest,
                    room=room,
                    check_in=start_date,
                    check_out=end_date,
                    # Set other fields as needed
                )

                # Update room status to "Occupied"
                room.status = 'Occupied'
                room.save()

                return redirect('success_page')  # Redirect to a success page

    else:
        form = ReservationForm()

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
        selected_room = request.POST.get('selected_room')
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

        # Send a JsonResponse indicating success
        response_data = {'success': True}

        # Add details for the alert box
        response_data['alert_message'] = f"Status of room {selected_room} changed to {selected_status}"

        return JsonResponse(response_data)
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
