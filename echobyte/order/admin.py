from django.contrib import admin
from .models import Cart, CartItems, Order, OrderItem, ReturnOrder

admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(ReturnOrder)
