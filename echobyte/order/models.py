from django.db import models
from django.contrib.auth.models import User
from product.models import Product, ProductVariant


# Create your models here.
class Cart(models.Model):
    owner = models.OneToOneField(User,on_delete=models.CASCADE)
    
class CartItems(models.Model):
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name = 'added_products')
    quantity = models.PositiveIntegerField(default = 1)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE, related_name = 'added_cart_items')
    created_at = models.DateTimeField(auto_now_add=True, null = True)
    
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
    ORDER_CONFIRMED = 1
    ORDER_SHIPPED = 2
    ORDER_DELIVERED = 3
    ORDER_CANCELLED = -1
    ORDER_CANCELLED_BY_SELLER = -2
    ORDER_STATUS_CHOICES = (
        (ORDER_CONFIRMED, 'Confirmed'),
        (ORDER_SHIPPED, 'Shipped'),
        (ORDER_DELIVERED, 'Delivered'),
        (ORDER_CANCELLED, 'Cancelled'),
        (ORDER_CANCELLED_BY_SELLER, 'Seller Cancelled')
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name = 'order_items')
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    amount =  models.DecimalField( max_digits=10, decimal_places=2)
    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=ORDER_CONFIRMED)
    address = models.CharField( max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

     
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

     
     

    
     



         
     
     
    
    


    
