# Generated by Django 4.2.7 on 2024-02-10 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_remove_address_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='landmark',
        ),
    ]