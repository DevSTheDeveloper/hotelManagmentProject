# Generated by Django 4.2.5 on 2023-09-21 19:33

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
            name='Guest',
            fields=[
                ('guest_fname', models.CharField(max_length=100)),
                ('guest_sname', models.CharField(max_length=100)),
                ('guest_id', models.CharField(max_length=4, primary_key=True, serialize=False, unique=True)),
            ],
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
        ),
        migrations.CreateModel(
            name='services',
            fields=[
                ('service_id', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('service_name', models.CharField(max_length=60)),
                ('service_desc', models.CharField(max_length=200)),
                ('service_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('staffId', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('f_name', models.CharField(max_length=50)),
                ('l_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=320)),
                ('phone', models.CharField(max_length=20)),
                ('position', models.CharField(max_length=50)),
                ('department', models.CharField(max_length=50)),
                ('is_manager', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='StaffLogin',
            fields=[
                ('staff', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='hotel.staff')),
                ('password', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('guest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotel.guest')),
                ('room_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.roomdata')),
            ],
        ),
        migrations.CreateModel(
            name='ReservationServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_reservation_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('reservation_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.services')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateTimeField(default=django.utils.timezone.now, validators=[hotel.models.validate_future_date])),
                ('check_out', models.DateTimeField(default=hotel.models.get_default_checkout_time, validators=[hotel.models.validate_future_date])),
                ('reservation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.guest')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.room')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('payment_type', models.CharField(choices=[('incoming', 'Incoming'), ('outgoing', 'Outgoing')], max_length=10)),
                ('from_customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.guest')),
                ('to_staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.staff')),
            ],
        ),
        migrations.CreateModel(
            name='GuestData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_phone', models.CharField(max_length=20)),
                ('guest_email', models.CharField(max_length=320)),
                ('guest_address', models.CharField(max_length=200)),
                ('guest_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.guest')),
            ],
        ),
    ]
