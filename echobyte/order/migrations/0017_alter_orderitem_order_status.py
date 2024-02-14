# Generated by Django 4.2.7 on 2024-02-14 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_alter_orderitem_address_alter_orderitem_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='order_status',
            field=models.IntegerField(choices=[(1, 'Confirmed'), (2, 'Shipped'), (3, 'Delivered'), (-1, 'Cancelled'), (-2, 'Seller Cancelled'), (4, 'Return Requested'), (5, 'Returned')], default=1),
        ),
    ]