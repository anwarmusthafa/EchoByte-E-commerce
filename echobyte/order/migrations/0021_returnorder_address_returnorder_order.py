# Generated by Django 4.2.7 on 2024-02-15 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_remove_address_landmark'),
        ('order', '0020_alter_orderitem_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='returnorder',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.address'),
        ),
        migrations.AddField(
            model_name='returnorder',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.orderitem'),
        ),
    ]
