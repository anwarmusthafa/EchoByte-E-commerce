# Generated by Django 5.0.1 on 2024-03-04 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_category'),
        ('coupon', '0007_category_offer'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category_offer',
            new_name='CategoryOffer',
        ),
    ]