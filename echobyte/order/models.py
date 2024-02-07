from django.db import models
from django.contrib.auth.models import User
from product.models import Product, ProductVariant

# Create your models here.
class Cart(models.Model):
    owner = models.OneToOneField(User,on_delete=models.CASCADE)
    sub_total = models.FloatField()
    def calculate_subtotal(self):
        cart_items = self.cartitems_set.all()
        subtotal = sum(item.total_price for item in cart_items)
        return subtotal

    def save(self, *args, **kwargs):
        self.sub_total = self.calculate_subtotal()
        super(Cart, self).save(*args, **kwargs)
    def __str__(self):
            return self.owner.customer.name +"'s Cart"
class CartItems(models.Model):
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name = 'added_products')
    quantity = models.PositiveIntegerField(default = 1)
    total_price = models.FloatField()
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE, related_name = 'added_cart_items')
    def __str__(self):
        return self.cart.owner.customer.name + "'s cart items"
    
    

    
