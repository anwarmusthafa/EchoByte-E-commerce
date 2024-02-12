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
    cart = get_object_or_404(Cart, owner=user)
    cart_items = CartItems.objects.filter(cart=cart).order_by('-created_at')
    address = Address.objects.filter(user=user)
    
    if request.method == 'POST':
        address_id = request.POST.get('address')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('paymentOption')
        
        if not address_id:
            # Address not selected, return an error message
            error_message = "Please select an address."
            return render(request, 'checkout.html', {'cart': cart, 'cart_items': cart_items, 'address': address, 'error_message': error_message})
        
        try:
            address_obj = Address.objects.get(pk=address_id)
        except Address.DoesNotExist:
            # Address not found, return an error message
            error_message = "The selected address does not exist."
            return render(request, 'checkout.html', {'cart': cart, 'cart_items': cart_items, 'address': address, 'error_message': error_message})
        
        try:
            # Create the order transactionally
            with transaction.atomic():
                order = Order.objects.create(owner=user, cart=cart, amount=amount, payment_method=payment_method)
                print('created order')
                for cart_item in cart_items:
                    amount = cart_item.quantity * cart_item.product.selling_price
                    OrderItem.objects.create(order=order, product=cart_item.product, address=address_obj, quantity=cart_item.quantity, amount=amount)
                    product = cart_item.product
                    product.stock -= cart_item.quantity
                    product.save()



                
                # Optionally, you can clear the cart after successful checkout
                cart_items.delete()
                cart.delete()

            # Redirect to the order success page or any other page
            return redirect('order_success')  # Replace 'order_success' with your actual URL name
        
        except Exception as e:
            print(e)
            # Handle any other exceptions, such as database errors
            error_message = "An error occurred while processing your order. Please try again later."

            return render(request, 'checkout.html', {'cart': cart, 'cart_items': cart_items, 'address': address, 'error_message': error_message})

    return render(request, 'checkout.html', {'cart': cart, 'cart_items': cart_items, 'address': address})
def order_success(request):
    
    return render(request,'order_success.html')
def list_orders(request):
    orders = OrderItem.objects.all().order_by('-created_at')
    context = {'orders':orders}
    return render(request, 'list-orders.html', context)
def order_cancel_by_seller(request, pk):
    # Retrieve the order object or return a 404 error if not found
    order = get_object_or_404(OrderItem, pk=pk)
    
    # Check if the request method is POST
    if request.method == 'POST':
        # Extract the status from the form data
        status = int(request.POST.get('status'))
        
        # Check if the provided status is valid (if needed)
        # For example, you might want to check if status == -2 is a valid status
        
        # Update the order status and save
        order.order_status = status
        order.save()
        product = order.product
        product.stock += order.quantity
        product.save()
    
    # Redirect to the list_orders view after processing
    return redirect('list_orders')




        







