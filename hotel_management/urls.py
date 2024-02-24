from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views  # Import Django's authentication views
from hotel.views import login_view, redirect_to_rooms, redirect_to_homepage, get_all_guests
from hotel import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='login.html'), name='root'),  
    path('admin/', admin.site.urls),
    path('homepage/', TemplateView.as_view(template_name='homepage.html'), name='homepage'),
    path('login/', login_view, name='login_view'),
    path('rooms/', views.rooms_views, name='rooms'),
    path('redirect-to-homepage/', redirect_to_homepage, name='redirect_to_homepage'),
    path('update_room_status/', views.update_room_status, name='update_room_status'),
    path('reservations/', views.make_reservation, name='make_reservation'),
    path('guests/', TemplateView.as_view(template_name='guest.html'), name='guest_page'),


    # Add the URL pattern for logout
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # To search for guest details 
    path('api/get_all_guests/', get_all_guests, name='get_all_guests'),

    
        # Add the URL patterns for password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Add the URL patterns for password change
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    
]
