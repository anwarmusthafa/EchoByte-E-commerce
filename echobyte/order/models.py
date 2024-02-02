from django.db import models
from django.contrib.auth.models import User
from product.models import Product, ProductVariant

# Create your models here.
class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    sub_total = models.FloatField()
    is_order_placed = models.BooleanField(default = False)
class CartItems(models.Model):
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name = 'added_carts')
    quantity = models.PositiveIntegerField(default = 1)
    total_price = models.FloatField()
    cart = models.ForeignKey(Cart,  on_delete=models.CASCADE)

    
