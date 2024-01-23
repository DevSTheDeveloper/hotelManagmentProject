from django.contrib import admin
from .models import CustomStaff, Guest, GuestData, RoomData, Room, Reservation, Service, Payment, ReservationServices

admin.site.register(CustomStaff)
admin.site.register(Guest)
admin.site.register(GuestData)
admin.site.register(RoomData)
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Service)
admin.site.register(Payment)
admin.site.register(ReservationServices)
