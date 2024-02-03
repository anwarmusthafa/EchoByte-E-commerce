from django.shortcuts import render , redirect
from .models import Cart,CartItems 
from product.models import Product, ProductVariant, ProductImage
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def cart(request):
    user = request.user
    try:
        cart_items = CartItems.objects.filter(cart__owner=user)
        context = {'cart_items': cart_items}
    except ObjectDoesNotExist:
        context = {'cart_items': None}  # Setting cart_items to None when cart is empty
    return render(request, 'cart.html', context)
from django.shortcuts import redirect

def add_to_cart(request):
    if request.POST:
        user = request.user
        customer = user
        quantity = request.POST.get('quantity') 
        product_id = request.POST.get('product-id')
        product = ProductVariant.objects.get(pk=product_id)
        print(quantity)
        cart_obj, created = Cart.objects.get_or_create(owner=customer, is_order_placed=False)
        cart_item = CartItems.objects.create(product=product, cart=cart_obj, quantity=1, total_price=1)
    return redirect(request.META.get('HTTP_REFERER', 'cart'))

        







