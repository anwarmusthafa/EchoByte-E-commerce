from django.db import models
from django.contrib.auth.models import User
from product.models import Product, ProductVariant

# Create your models here.
class Cart(models.Model):
    owner = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
            return self.owner.customer.name +"'s Cart"
class CartItems(models.Model):
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name = 'added_products')
    quantity = models.PositiveIntegerField(default = 1)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE, related_name = 'added_cart_items')
    created_at = models.DateTimeField(auto_now_add=True, null = True)
    def __str__(self):
        return self.cart.owner.customer.name + "'s cart items"
    
    


    
