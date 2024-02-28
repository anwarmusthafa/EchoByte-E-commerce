from django import template
from decimal import Decimal
register = template.Library()

@register.filter(name='sub_total_of_cart')
def sub_total_of_cart(cart, discount_percentage=None):
    total = Decimal('0')  # Initialize total as Decimal
    for cart_item in cart.added_cart_items.all():
        total += cart_item.quantity * cart_item.product.selling_price
    
    if discount_percentage:
        discount_amount = total * (Decimal(discount_percentage) / Decimal('100'))  # Convert discount_percentage to Decimal
        total -= discount_amount
    return float(total)
