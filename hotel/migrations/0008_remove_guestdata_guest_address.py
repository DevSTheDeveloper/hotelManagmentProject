# Generated by Django 4.2.5 on 2024-02-19 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0007_remove_customstaff_groups_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guestdata',
            name='guest_address',
        ),
    ]