# Generated by Django 5.0.1 on 2024-02-07 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_remove_cart_sub_total_remove_cartitems_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
