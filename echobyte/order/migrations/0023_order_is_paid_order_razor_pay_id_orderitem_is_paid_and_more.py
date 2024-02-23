# Generated by Django 5.0.1 on 2024-02-23 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0022_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='razor_pay_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='is_paid',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='payment_method',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='razor_pay_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]