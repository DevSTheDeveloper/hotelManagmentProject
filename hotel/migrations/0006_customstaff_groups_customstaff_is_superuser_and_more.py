# Generated by Django 4.2.5 on 2024-02-05 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('hotel', '0005_merge_0003_staffdata_0004_rename_staff_customstaff'),
    ]

    operations = [
        migrations.AddField(
            model_name='customstaff',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='custom_staff_set', related_query_name='custom_staff', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='customstaff',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AddField(
            model_name='customstaff',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='customstaff',
            name='password',
            field=models.CharField(default='default_password', max_length=128),
        ),
        migrations.AddField(
            model_name='customstaff',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='custom_staff_set', related_query_name='custom_staff', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AlterModelTable(
            name='customstaff',
            table=None,
        ),
    ]