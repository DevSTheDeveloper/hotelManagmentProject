import os
import django
from django.conf import settings
from hotel.models import Room  # Import your Room model from the 'hotel' app

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')

# Initialize Django
django.setup()

def query_database():
    # Query the database for room 106
    room = Room.objects.get(room_number=106)

    # Print the room's status
    print(room.status)

if __name__ == '__main__':
    query_database()
