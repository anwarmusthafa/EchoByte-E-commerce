from django.shortcuts import render , redirect, get_object_or_404
from .models import Cart,CartItems 
from product.models import Product, ProductVariant, ProductImage
from .models import Cart,CartItems
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

# Create your views here.

def cart(request):
    user = request.user
    try:
        cart_items = CartItems.objects.filter(cart__owner=user)
        cart = Cart.objects.get(owner=user)
        context = {'cart_items': cart_items,'cart':cart}
    except ObjectDoesNotExist:
        context = {'cart_items': None} 
    return render(request, 'cart.html', context)

def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        customer = user
        quantity = int(request.POST.get('quantity',1) )
        product_id = int(request.POST.get('product-id'))
        product = ProductVariant.objects.get(pk=product_id)
        cart_obj, created = Cart.objects.get_or_create(owner=customer)
        cart_item = CartItems.objects.create(product=product, cart=cart_obj, quantity=quantity,)
        success_message = 'Product added to cart successfully.'
        return JsonResponse({'success_message': success_message})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
def delete_cart_item(request,pk):
    cart_item = get_object_or_404(CartItems, pk=pk)
    cart_item.delete()
    return redirect('cart')
def add_cart_item_quantity(request,pk):
    cart_item = CartItems.objects.get(pk=pk)
    print(cart_item.quantity)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')
def sub_cart_item_quantity(request,pk):
    cart_item = CartItems.objects.get(pk=pk)
    print(cart_item.quantity)
    cart_item.quantity -= 1
    cart_item.save()
    return redirect('cart')




        







