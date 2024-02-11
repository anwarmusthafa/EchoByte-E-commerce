from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart,CartItems,Order,OrderItem
from customer.models import Address, Customer
from product.models import Product, ProductVariant, ProductImage
from .models import Cart,CartItems
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.db import transaction


# Create your views here.
@login_required(login_url='signin')
def cart(request):
    user = request.user
    try:
        cart_items = CartItems.objects.filter(cart__owner=user).order_by('-created_at')
        cart = Cart.objects.get(owner=user)
        context = {'cart_items': cart_items,'cart':cart}
    except ObjectDoesNotExist:
        context = {'cart_items': None} 
    return render(request, 'cart.html', context)

@login_required(login_url='signin')
def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        customer = user
        quantity = int(request.POST.get('quantity', 1))
        product_id = int(request.POST.get('product-id'))
        product = ProductVariant.objects.get(pk=product_id)
        cart_obj, created = Cart.objects.get_or_create(owner=customer)
        cart_item = CartItems.objects.create(product=product, cart=cart_obj, quantity=quantity)
        success_message = 'Product added to cart successfully.'
        return JsonResponse({'success_message': success_message})
    else:
        # If it's not a POST request, return a JSON response indicating the need to sign in
        return JsonResponse({'redirect_url': reverse('signin')})
@login_required(login_url='signin')
def delete_cart_item(request,pk):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItems, pk=pk)
        cart_item.delete()
        return redirect('cart')
    
@login_required(login_url='signin')
def add_cart_item_quantity(request,pk):
    if request.user.is_authenticated:
        cart_item = CartItems.objects.get(pk=pk)
        if cart_item.quantity >= 4:
            messages.error(request, "Only 4 item can buy one order")
        else: 
            cart_item.quantity += 1
            cart_item.save()
        return redirect('cart')
@login_required(login_url='signin')
def sub_cart_item_quantity(request, pk):
    if request.user.is_authenticated:
        cart_item = CartItems.objects.get(pk=pk)
        if cart_item.quantity <= 1:
            messages.error(request, "At least one item is needed in the order.")
        else:
            cart_item.quantity -= 1
            cart_item.save()
        return redirect('cart')


def checkout(request):
    user = request.user
    cart = Cart.objects.get(owner=user)
    if request.POST:
        address = request.POST.get('address')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('paymentOption')
        
        # Create the order
        with transaction.atomic():
            order = Order.objects.create(owner=user, cart=cart, amount=amount, payment_method=payment_method)
            # Iterate through cart items and create order items
            for cart_item in cart.added_cart_items.all():
                amount = cart_item.quantity * cart_item.product.selling_price
                # Create the order item and save price
                OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity, amount=amount)
        
        # Optionally, you can clear the cart after checkout
        # cart.added_cart_items.all().delete()

        # Redirect to order success page or any other page
        return redirect('order_success')  # Replace 'order_success' with your actual URL name

    cart_items = CartItems.objects.filter(cart__owner=user).order_by('-created_at')
    address = Address.objects.filter(user=user)
    context = {'cart': cart, 'cart_items': cart_items, 'address': address}
    return render(request, 'checkout.html', context)
def order_success(request):
    
    return render(request,'order_success.html')




        







