from django.db.models.signals import post_save ,post_delete
from django.dispatch import receiver
from product.models import *
from .models import CategoryOffer
from decimal import Decimal

@receiver(post_save, sender=CategoryOffer)
def apply_category_offer(sender, instance, created, **kwargs):
    if created or instance.offer_percentage != instance._previous_offer_percentage:
        products = ProductVariant.objects.filter(product__category=instance.category)
        for product in products:
            offer_percentage_decimal = Decimal(instance.offer_percentage) / Decimal(100)
            new_price = product.selling_price * (Decimal(1) - offer_percentage_decimal)
            product.selling_price = new_price.quantize(Decimal('0.01'))  # Ensure two decimal places
            product.save()

@receiver(post_delete, sender=CategoryOffer)
def revert_category_offer(sender, instance, **kwargs):
    products = ProductVariant.objects.filter(product__category=instance.category)
    for product in products:
        offer_percentage_decimal = Decimal(instance.offer_percentage) / Decimal(100)
        original_price = product.selling_price / (Decimal(1) - offer_percentage_decimal)
        product.selling_price = original_price.quantize(Decimal('0.01'))  # Ensure two decimal places
        product.save()