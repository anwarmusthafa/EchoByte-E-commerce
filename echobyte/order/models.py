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
class Order(models.Model):
    ORDER_CONFIRMED = 1
    ORDER_SHIPPED = 2
    ORDER_DELIVERED = 3
    ORDER_CANCELLED = -1
    ORDER_STATUS_CHOICES = (
        (ORDER_CONFIRMED, 'ORDER_CONFIRMED'),
        (ORDER_SHIPPED, 'ORDER_SHIPPED'),
        (ORDER_DELIVERED, 'ORDER_DELIVERED'),
        (ORDER_CANCELLED, 'ORDER_CANCELLED')
    )

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField(ProductVariant, through='OrderItem')
    amount =  models.DecimalField( max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=ORDER_CONFIRMED)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    amount =  models.DecimalField( max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"
     
# class OrderedProduct(models.Model):
#      ORDER_CONFIRMED = 1
#      ORDER_SHIPPED = 2
#      ORDER_DELIVERED = 3
#      ORDER_CANCELLED = -1
#      ORDER_STATUS_CHOICES = ((ORDER_CONFIRMED, 'ORDER_CONFIRMED'),
#                              (ORDER_SHIPPED, 'ORDER_SHIPPED'),
#                              (ORDER_DELIVERED, 'ORDER_DELIVERED'),
#                              (ORDER_CANCELLED, 'ORDER_CANCELLED'))
#      owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank = True, related_name = 'ordered_products')
#      product = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank = True, related_name = 'orders')
#      quantity = models.PositiveIntegerField()
#      amount =  models.DecimalField( max_digits=10, decimal_places=2)
#      order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=ORDER_CONFIRMED)
#      order = models.ForeignKey(Order,  on_delete=models.CASCADE)
#      created_at = models.DateTimeField(auto_now_add=True, null = True)
#      updated_at = models.DateTimeField(auto_now=True)

     
     

    
     



         
     
     
    
    


    
