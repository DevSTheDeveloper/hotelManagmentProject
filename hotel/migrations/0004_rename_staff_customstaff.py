# Generated by Django 4.2.5 on 2024-01-23 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0003_staffdata'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Staff',
            new_name='CustomStaff',
        ),
    ]