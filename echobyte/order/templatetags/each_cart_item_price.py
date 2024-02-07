from django import template
register = template.Library()
@register.filter(name='each_cart_item_price')
def eaah_cart_item_price(selling_price,quantity):
    return selling_price * quantity
