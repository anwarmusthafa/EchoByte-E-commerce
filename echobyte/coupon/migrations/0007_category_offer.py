# Generated by Django 5.0.1 on 2024-03-04 06:36

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_category'),
        ('coupon', '0006_delete_categoryoffer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category_offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('offer_percentage', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('is_listed', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
            ],
        ),
    ]
