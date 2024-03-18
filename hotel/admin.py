from django.contrib import admin
from .models import CustomStaff, HotelGuest, RoomData, Room, Reservation, Service, Payment, ReservationServices

admin.site.register(CustomStaff)
admin.site.register(HotelGuest)
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Service)
admin.site.register(Payment)
