from django import template
register = template.Library()
@register.filter(name='sub_total_of_cart')
def eaah_cart_item_price(cart, coupon_pertentage = None):
    total = 0
    for cart_item in cart.added_cart_items.all():
        total += cart_item.quantity * cart_item.product.selling_price
    
    if coupon_pertentage:
        discount_amount = total * (coupon_pertentage / 100)
        total -= discount_amount
        
    return total

