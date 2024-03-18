# Generated by Django 4.2.5 on 2024-02-24 21:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import hotel.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomStaff',
            fields=[
                ('staff_id', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('f_name', models.CharField(max_length=50)),
                ('l_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=320)),
                ('phone', models.CharField(max_length=20)),
                ('position', models.CharField(max_length=50)),
                ('department', models.CharField(max_length=50)),
                ('is_manager', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'hotel_staff',
            },
        ),
        migrations.CreateModel(
            name='HotelGuest',
            fields=[
                ('guest_fname', models.CharField(max_length=100)),
                ('guest_sname', models.CharField(max_length=100)),
                ('guest_id', models.CharField(max_length=4, primary_key=True, serialize=False, unique=True)),
                ('guest_email', models.EmailField(max_length=320)),
            ],
            options={
                'db_table': 'hotel_guest',
            },
        ),
        migrations.CreateModel(
            name='RoomData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=10, unique=True)),
                ('rate_per_night', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('beds', models.PositiveIntegerField()),
                ('capacity', models.PositiveIntegerField()),
                ('has_balcony', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'hotel_room_data',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('service_id', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('service_name', models.CharField(max_length=60)),
                ('service_desc', models.CharField(max_length=200)),
                ('service_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'hotel_services',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_number', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=20)),
                ('guest_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotel.hotelguest')),
            ],
            options={
                'db_table': 'hotel_room',
            },
        ),
        migrations.CreateModel(
            name='ReservationServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_reservation_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('reservation_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.service')),
            ],
            options={
                'db_table': 'hotel_reservation_services',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateTimeField(default=django.utils.timezone.now, validators=[hotel.models.validate_future_date])),
                ('check_out', models.DateTimeField(default=hotel.models.get_default_checkout_time, validators=[hotel.models.validate_future_date])),
                ('reservation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotelguest')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.room')),
            ],
            options={
                'db_table': 'hotel_reservation',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('payment_type', models.CharField(choices=[('incoming', 'Incoming'), ('outgoing', 'Outgoing')], max_length=10)),
                ('from_customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.hotelguest')),
                ('to_staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.customstaff')),
            ],
            options={
                'db_table': 'hotel_payment',
            },
        ),
    ]
