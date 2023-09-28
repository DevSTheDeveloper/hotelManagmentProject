# views.py

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Room
from django.db import transaction

def login_view(request):
    if request.method == 'POST':
        staff_id = request.POST['staffId']
        password = request.POST['password']

        with transaction.atomic():  # Use a transaction block
            user = authenticate(request, username=staff_id, password=password)

            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                return render(request, 'login.html', {'error_message': 'Invalid credentials'})

    return render(request, 'login.html')


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
