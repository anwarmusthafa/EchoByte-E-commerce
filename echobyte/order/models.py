from django.db import models
from django.contrib.auth.models import User
from product.models import Product, ProductVariant

# Create your models here.
class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    sub_total = models.FloatField(default = 0)
    is_order_placed = models.BooleanField(default = False)
    def __str__(self):
            return self.owner.customer.name +"'s Cart"
    
class CartItems(models.Model):
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name = 'added_carts')
    quantity = models.PositiveIntegerField(default = 1)
    total_price = models.FloatField()
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    def __str__(self):
        return self.cart.owner.customer.name + "'s cart items"
    
    

    
