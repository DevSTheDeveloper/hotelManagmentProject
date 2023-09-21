from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='login.html'), name='home'),  # Set 'login.html' as the homepage
    path('admin/', admin.site.urls),
    # Add other app-specific URLs as needed
]
