from django.db import models
from django.contrib.auth.models import User
from product.models import Product, ProductVariant
from customer.models import Address


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
    ORDER_RETURN_REQUESTED = 4
    ORDER_RETURNED = 5
    ORDER_CANCELLED = -1
    ORDER_CANCELLED_BY_SELLER = -2

    ORDER_STATUS_CHOICES = (
        (ORDER_CONFIRMED, 'Confirmed'),
        (ORDER_SHIPPED, 'Shipped'),
        (ORDER_DELIVERED, 'Delivered'),
        (ORDER_CANCELLED, 'Cancelled'),
        (ORDER_CANCELLED_BY_SELLER, 'Cancelled by Seller'),
        (ORDER_RETURN_REQUESTED, 'Return Requested'),
        (ORDER_RETURNED, 'Returned')
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=ORDER_CONFIRMED)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


class ReturnOrder(models.Model):
    RETURN_REQUESTED = 1
    RETURNED = 2
    STATUS_CHOICES = ((RETURN_REQUESTED, 'Return Requested'),
        (RETURNED,'Returned'))
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null = True, blank = True)
    product = models.ForeignKey(ProductVariant,on_delete=models.SET_NULL, blank = True, null = True)
    order = models.ForeignKey(OrderItem,on_delete=models.SET_NULL, null = True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    reason = models.TextField()
    amount_to_refund = models.DecimalField( max_digits=10, decimal_places=2)
    return_status = models.IntegerField(choices=STATUS_CHOICES, default=RETURN_REQUESTED)
    created_at = models.DateTimeField(auto_now_add=True)

     



     
     

    
     



         
     
     
    
    


    
