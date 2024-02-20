from django import template
from decimal import Decimal
register = template.Library()

@register.filter(name='calculate_discount_amount')
def calculate_discount_amount(cart, discount_percentage=None):
    if discount_percentage:
        total = Decimal('0')
        for cart_item in cart.added_cart_items.all():
            total += cart_item.quantity * cart_item.product.selling_price
        discount_amount = total * (Decimal(discount_percentage) / Decimal('100'))
        return float(discount_amount)
    else:
        return Decimal('0')
