import logging
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Room, HotelGuest
from .models import Reservation 
from .forms import ReservationForm
from . import views, models
from .models import HotelGuest
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from datetime import timedelta



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


from django.shortcuts import render, redirect
from .forms import ReservationForm

def reservation_view(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., save it to a database)
            return redirect('reservation.html')
    else:
        form = ReservationForm()

    return render(request, 'reservation.html', {'form': form})

def generate_unique_user_id():
    while True:
        user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not Guest.objects.filter(user_id=user_id).exists():
            return user_id

@csrf_protect
def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)

        if form.is_valid():
            # Extract form data
            room_type = form.cleaned_data['room_type']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            guest_email = form.cleaned_data['guest_email']

            # Check if the guest with the given email already exists in hotel_guest_data
            try:
                guest_data = HotelGuest.objects.get(guest_email=guest_email)
                guest_id = guest_data.guest_id_id
            except HotelGuest.DoesNotExist:
                # Guest does not exist in hotel_guest_data, return an error response
                return JsonResponse({'error': "Email doesn't exist, please create the guest and enter details on 'Guest' tab."}, status=400)

            with transaction.atomic():
                # Check room availability - ie is room == 'avaliable'
                try:
                    room = Room.objects.select_for_update().get(room_type=room_type, status='Available')
                except Room.DoesNotExist:
                    return JsonResponse({'error': 'No rooms available of this type'}, status=400)

                room.guest_id_id = guest_id
                room.save()


                return JsonResponse({'success': 'Reservation successfully created'}, status=200)

    else:
        form = ReservationForm()

    return render(request, 'reservations.html', {'form': form})


from django.http import JsonResponse
from .models import Room, Payment
from django.utils import timezone

def initiate_room_payment(request, room_number):
    try:
        # Get the selected room
        room = Room.objects.get(room_number=room_number)

        # Determine the room price based on whether the room number is odd or even
        if room_number % 2 == 0:  # Even room number
            original_price = 150
        else:  # Odd room number
            original_price = 200

        # Calculate the new total price (original price)

        payment = Payment.objects.create(
            amount=original_price,
            payment_date=timezone.now(),
            payment_type='outgoing',  
            from_customer=HotelGuest.guest_id, 
        )

        return JsonResponse({'success': True, 'message': 'Room payment initiation successful'})

    except Room.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Room not found'})


def initiate_new_payment(request, room_number):
    try:
        # Get the selected room
        room = Room.objects.get(room_number=room_number)

        # Get the original room price
        original_price = room.price

        # Get the total services selected by the guest
        selected_services = request.POST.getlist('services')
        total_services_price = sum([float(service_data['price']) for service_data in selected_services])

        # Calculate the new total price (original price + services)
        new_total_price = original_price + total_services_price

        # Save payment information to the database
        payment = payment.objects.create(
            room=room,
            original_price=original_price,
            services_price=total_services_price,
            new_total_price=new_total_price
        )

        return JsonResponse({'success': True, 'message': 'Payment initiation successful'})

    except Room.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Room not   found'})
    
    except HotelGuest.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Guest not found'})


#Used in guests.html - the search contents will be the names and email.
def get_all_guests(request):
    search_term = request.GET.get('search', '')
    
    guests = HotelGuest.objects.filter(
        guest_fname__icontains=search_term) | \
        HotelGuest.objects.filter(guest_sname__icontains=search_term) | \
        HotelGuest.objects.filter(guest_email__icontains=search_term)

    guest_list = []

    for guest in guests:
        guest_list.append({
            'guest_fname': HotelGuest.guest_fname,
            'guest_sname': HotelGuest.guest_sname,
            'guest_id': HotelGuest.objects.get(guest_id=guest.guest_id).guest_email,
            'guest_email': HotelGuest.guest_email
        })

    return JsonResponse(guest_list, safe=False)


#used in Rooms.html for data retrieval 
def get_guest_data(request):

    guest_data = {
        'guest_name': HotelGuest.guest_fnamename,
        'guest_id': HotelGuest.guest_id,
        'email': HotelGuest.guest_email,
    }

    return render(request, 'guest_data.html', {'guest_data': guest_data})



def remove_guest(request):
    guest_id = Room.guest_id 
    now == datetime.now()

    try:
        # Fetch the guest based on the guest_id
        guest = HotelGuest.objects.get(guest_id=guest_id)

        # Perform cascade deletion: remove related reservations
        reservations = Reservation.objects.filter(Q(guest=guest) or Q(check_out__date=now.date()))
        reservations.delete()

        # Finally, remove the guest
        Room.guest_id.delete()

        return HttpResponse("Guest removed successfully with cascade deletion.")
    except Guest.DoesNotExist:
        return HttpResponse("Guest not found.")
    except Exception as e:
        return HttpResponse(f"Error: {e}")



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
            room = Room.objects.get(room_number=selected_room)
        except Room.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Room not found'})

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



def create_guest_view(request):
    if request.method == 'POST':
        guest_fname = request.POST.get('guest_fname')
        guest_sname = request.POST.get('guest_sname')
        guest_email = request.POST.get('guest_email')

        guest_id = [] #created as an array which will be iterated 
        
        guest = HotelGuest.objects.create(
            guest_fname=guest_fname,
            guest_sname=guest_sname,
            guest_id=guest_id[i+1],
            guest_email=guest_email
        )

