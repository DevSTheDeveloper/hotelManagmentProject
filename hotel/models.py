#Please note: i have defined __str__ functions within the model.py file so i can test my db as well as its functionality/readability while i develop it. - it is reccomended by django to do this.
#In Django we use models.py in order to define fields/tables - django then creates a .db file for you once all classes/tables have been defined, as well as defining their paramaters/datatypes

from datetime import timedelta #this library retrieves the date and time now or in the future. 
import string
import uuid #this will allow the system to generate a unique reservationID - using the time,date,MAC address for a unique identifier 
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import random



class Guest(models.Model):
    guest_fname = models.CharField(max_length=100)
    guest_sname = models.CharField(max_length=100)
    guest_id = models.CharField(primary_key=True, max_length=4, unique=True)

class GuestData(models.Model):
    guest_id = models.ForeignKey(Guest, on_delete=models.CASCADE)
    guest_phone = models.CharField(max_length=20)
    guest_email = models.CharField(max_length=320) 
    guest_address = models.CharField(max_length=200)

class RoomData(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    rate_per_night = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    beds = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    has_balcony = models.BooleanField(default=False)

class Room(models.Model):
    room_number = models.ForeignKey(RoomData, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    guest = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True, blank=True)

def get_default_checkout_time():
    return timezone.now() + timedelta(days=1) #Default checkout date is the day after the check in. I have not enforced a time limit (ie. before 11AM) due to coding issues



# Custom validator function to check if a date is in the past
def validate_future_date(value):
    if value < timezone.now():
        raise ValidationError('Date cannot be in the past.')

class Reservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField(default=timezone.now, validators=[validate_future_date])
    check_out = models.DateTimeField(default=get_default_checkout_time, validators=[validate_future_date])
    reservation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Reservation #{self.id} - Guest: {self.guest}, Room: {self.room}"


class Staff(models.Model):
    staffId = models.CharField(primary_key=True, max_length=3)
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=320)
    phone = models.CharField(max_length=20)
    position = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    is_manager = models.BooleanField(default=False)

    def __str__(self):
        return f"Staff #{self.staffId} - {self.f_name} {self.l_name}"


class services(models.Model):
    service_id = models.CharField(primary_key=True, max_length=2) # 99 service slots, although most won't be used - 2 digit number
    service_name = models.CharField(max_length=60)
    service_desc = models.CharField(max_length=200)
    service_price = models.DecimalField(max_digits=10, decimal_places=2) # set the price of a service, 10 digits available (max value: £99999999.99)

    def __str__(self):
        return self.service_name
    
class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing'),
    ]

    payment_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES)

    # Fields to represent sender and receiver
    from_customer = models.ForeignKey(Guest, on_delete=models.CASCADE, blank=True, null=True)  #for simplicty, only ingoing/outgoing payments are for staff or customers. 
    to_staff = models.ForeignKey(Staff, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        sender = self.from_customer if self.from_customer else self.to_staff
        receiver = self.to_staff if self.to_staff else self.from_customer
        return f"Payment #{self.payment_id} - Amount: {self.amount}, Type: {self.payment_type}, From: {sender}, To: {receiver}"    

def generate_unique_reservation_id():
    # Define the length of letters and digits in the ID - got help from chatGPT to generate that+
    num_letters = 3
    num_digits = 4

    # Generate random letters
    letters = ''.join(random.choice(string.ascii_uppercase) for _ in range(num_letters))

    # Generate random digits
    digits = ''.join(random.choice(string.digits) for _ in range(num_digits))

    # Combine letters and digits
    reservation_id = f"{letters}{digits}{letters}"

    # Check if the ID already exists in the database
    while Reservation.objects.filter(reservation_id=reservation_id).exists():
        # Regenerate if it already exists
        letters = ''.join(random.choice(string.ascii_uppercase) for _ in range(num_letters))
        digits = ''.join(random.choice(string.digits) for _ in range(num_digits))
        reservation_id = f"{letters}{digits}{letters}"

    return reservation_id

class ReservationServices(models.Model):
    service = models.ForeignKey(services, on_delete=models.CASCADE)
    service_reservation_id = models.UUIDField(default=uuid.uuid4, editable=False)
    
    reservation_id = models.UUIDField(default=uuid.uuid4, editable=False) # DJANGO has built-in UUID generators - it uses the current date and time/other variables to generate a unique ID.

    def __str__(self):
        return f"Reservation Service - Service: {self.service}, Reservation: {self.reservation}"

    def save(self, *args, **kwargs):
        #checks if the generated string is unique, compares it to - allows us to save the unique ID. - This is the same way I save data to fields on other tables. 
        if not self.reservation_id:
            self.reservation_id = generate_unique_reservation_id()
        super().save(*args, **kwargs)