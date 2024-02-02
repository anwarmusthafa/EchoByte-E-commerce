from django.shortcuts import render , redirect
from .models import Cart,CartItems 
from product.models import Product, ProductVariant
from decimal import Decimal

# Create your views here.

def cart(request):
    user = request.user
    cart_items = CartItems.objects.filter(cart__owner = user)
    context = {'cart_items':cart_items}
    return render(request, 'cart.html', context )
def add_to_cart(request):
    if request.POST:
        user = request.user
        customer = user
        quantity = request.POST.get('quantity') # Ensure quantity is converted to int
        product_id = request.POST.get('product-id')
        product = ProductVariant.objects.get(pk=product_id)
        print(quantity)
        cart_obj,created = Cart.objects.get_or_create( owner=customer,is_order_placed=False)
        cart_item = CartItems.objects.create( product=product, cart = cart_obj, quantity = 1 , total_price=10)
    return redirect('cart')
        







