from datetime import timedelta
import string
import uuid
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import random
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class StaffManager(BaseUserManager):
    def create_user(self, staff_id, password=None, **extra_fields):
        if not staff_id:
            raise ValueError('The Staff ID field must be set')
        user = self.model(staff_id=staff_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, staff_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(staff_id, password, **extra_fields)

class Staff(AbstractBaseUser, PermissionsMixin):
    staff_id = models.CharField(primary_key=True, max_length=3)
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=320)
    phone = models.CharField(max_length=20)
    position = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    is_manager = models.BooleanField(default=False)

    # Add the following lines to resolve the clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='staff_set',
        related_query_name='staff',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='staff_set',
        related_query_name='staff',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    objects = StaffManager()

    USERNAME_FIELD = 'staff_id'

    def __str__(self):
        return self.staff_id



class Guest(models.Model):
    guest_fname = models.CharField(max_length=100)
    guest_sname = models.CharField(max_length=100)
    guest_id = models.CharField(primary_key=True, max_length=4, unique=True)
    
    class Meta:
        db_table = 'hotel_guest'
        
class GuestData(models.Model):
    guest_id = models.ForeignKey(Guest, on_delete=models.CASCADE)
    guest_phone = models.CharField(max_length=20)
    guest_email = models.CharField(max_length=320) 
    guest_address = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'hotel_guest_data'

class RoomData(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    rate_per_night = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    beds = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    has_balcony = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'hotel_room_data'

class Room(models.Model):
    room_number = models.CharField(max_length=10, primary_key=True)
    status = models.CharField(max_length=20)
    guest_id = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'hotel_room'


def get_default_checkout_time():
    return timezone.now() + timedelta(days=1)

def validate_future_date(value):
    if value < timezone.now():
        raise ValidationError('Date cannot be in the past.')

class Reservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField(default=timezone.now, validators=[validate_future_date])
    check_out = models.DateTimeField(default=get_default_checkout_time, validators=[validate_future_date])
    reservation_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'hotel_reservation'
        
    def __str__(self):
        return f"Reservation #{self.id} - Guest: {self.guest}, Room: {self.room}"

class Staff(models.Model):
    staff_id = models.CharField(primary_key=True, max_length=3)
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=320)
    phone = models.CharField(max_length=20)
    position = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    is_manager = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'hotel_staff'

    def __str__(self):
        return f"Staff #{self.staff_id} - {self.f_name} {self.l_name}"

class Service(models.Model):
    service_id = models.CharField(primary_key=True, max_length=2)
    service_name = models.CharField(max_length=60)
    service_desc = models.CharField(max_length=200)
    service_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'hotel_services'

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
    from_customer = models.ForeignKey(Guest, on_delete=models.CASCADE, blank=True, null=True)
    to_staff = models.ForeignKey(Staff, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'hotel_payment'

    def __str__(self):
        sender = self.from_customer if self.from_customer else self.to_staff
        receiver = self.to_staff if self.to_staff else self.from_customer
        return f"Payment #{self.payment_id} - Amount: {self.amount}, Type: {self.payment_type}, From: {sender}, To: {receiver}"

def generate_unique_reservation_id():
    num_letters = 3
    num_digits = 4
    letters = ''.join(random.choice(string.ascii_uppercase) for _ in range(num_letters))
    digits = ''.join(random.choice(string.digits) for _ in range(num_digits))

    reservation_id = f"{letters}{digits}{letters}"

    while Reservation.objects.filter(reservation_id=reservation_id).exists():
        letters = ''.join(random.choice(string.ascii_uppercase) for _ in range(num_letters))
        digits = ''.join(random.choice(string.digits) for _ in range(num_digits))
        reservation_id = f"{letters}{digits}{letters}"

    return reservation_id

class ReservationServices(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    service_reservation_id = models.UUIDField(default=uuid.uuid4, editable=False)
    
    reservation_id = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        db_table = 'hotel_reservation_services'
        
    def __str__(self):
        return f"Reservation Service - Service: {self.service}, Reservation: {self.reservation}"

    def save(self, *args, **kwargs):
        if not self.reservation_id:
            self.reservation_id = generate_unique_reservation_id()
        super().save(*args, **kwargs)
