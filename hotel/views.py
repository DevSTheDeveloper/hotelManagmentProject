from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        staff_id = request.POST['employee_id']
        password = request.POST['password']

        # Authenticate using staffId as the username and default password 'password'
        user = authenticate(request, username=staff_id, password=password)

        if user is not None:
            # Login the user
            login(request, user)

            # Redirect to the homepage or any other desired page
            return redirect('homepage')
        else:
            # Handle invalid login credentials (e.g., show an error message)
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})

    return render(request, 'login.html')
