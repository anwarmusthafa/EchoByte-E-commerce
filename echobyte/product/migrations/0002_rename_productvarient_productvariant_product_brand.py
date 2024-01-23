# Generated by Django 5.0.1 on 2024-01-23 06:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductVarient',
            new_name='ProductVariant',
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.brand'),
        ),
    ]
