from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from hotel.views import login_view

urlpatterns = [
    path('', TemplateView.as_view(template_name='login.html'), name='login'),
    path('admin/', admin.site.urls),
    path('homepage/', TemplateView.as_view(template_name='homepage.html'), name='homepage'),  # Added a comma here
    path('login/', login_view, name='login_view'),  # Use the correct import path here
    
    # Add other app-specific URLs as needed
]
