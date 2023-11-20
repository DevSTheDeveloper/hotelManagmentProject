from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from hotel.views import login_view, redirect_to_rooms, redirect_to_homepage
from hotel import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='login.html'), name='root'),  
    path('admin/', admin.site.urls),
    path('homepage/', TemplateView.as_view(template_name='homepage.html'), name='homepage'),
    path('login/', login_view, name='login_view'),
    path('rooms/', views.rooms_views, name='rooms'),  # Updated view function name and URL pattern
    path('redirect-to-homepage/', redirect_to_homepage, name='redirect_to_homepage'),
    path('update_room_status/', views.update_room_status, name='update_room_status'),
    path('reservations/', views.make_reservation, name='make_reservation'),
]
