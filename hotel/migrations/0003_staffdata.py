# Generated by Django 4.2.5 on 2024-01-23 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_rename_services_service_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffData',
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
                'db_table': 'hotel_staff_data',
            },
        ),
    ]