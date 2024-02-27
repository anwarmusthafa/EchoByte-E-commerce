from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart,CartItems,Order,OrderItem, ReturnOrder
from customer.models import Address, Customer , Wallet
from product.models import Product, ProductVariant, ProductImage
from .models import Cart,CartItems, Wishlist
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseServerError, JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.db import transaction
import uuid
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Wishlist
from coupon.models import Coupon
import decimal
from django.db.models import Case, When, Value, IntegerField

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

from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required(login_url='signin')
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
        if not request.user.is_authenticated:
            # If user is not authenticated, return a JSON response indicating the need to sign in
            return JsonResponse('user not authenticated')
        else:
            # Handle other cases where it's not a POST request
            return JsonResponse({'error': 'Method not allowed'})

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

@login_required(login_url='signin')
def checkout(request):
    user = request.user
    cart = get_object_or_404(Cart, owner=user)
    cart_items = CartItems.objects.filter(cart=cart).order_by('-created_at')
    address = Address.objects.filter(user=user)
    coupons = Coupon.objects.filter(is_active = True)
    
    if request.method == 'POST':
        address_id = request.POST.get('address')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        discount_amount = request.POST.get('discount_amount', None)
        
        if not address_id:
            # Address not selected, return an error message
            error_message = "Please select an address."
            context = {'cart': cart, 'cart_items': cart_items, 'address': address, 'error_message': error_message}
            return render(request, 'checkout.html')
        
        try:
            address_obj = Address.objects.get(pk=address_id)
        except Address.DoesNotExist:
            # Address not found, return an error message
            error_message = "The selected address does not exist."
            context = {'cart': cart, 'cart_items': cart_items, 'address': address, 'error_message': error_message}
            return render(request, 'checkout.html')
        
        try:
            # Create the order transactionally
            with transaction.atomic():
                order = Order.objects.create(owner=user, cart=cart, amount=amount, payment_method=payment_method, discount_amount = discount_amount)
                if payment_method == 'online':
                        order.is_paid = True
                        order.razor_pay_id = razorpay_payment_id
                        order.save()
                for cart_item in cart_items:
                    def generate_unique_integer_id(length=8):
                        """
                        Generate a unique integer ID with the specified length.
                        """
                        # Generate a UUID
                        unique_id = uuid.uuid4().int

                        # Truncate or pad the integer to match the desired length
                        unique_id_str = str(unique_id)[:length].zfill(length)

                        return int(unique_id_str)
                    unique_order_id = generate_unique_integer_id(length=8)
                    amount = cart_item.quantity * cart_item.product.selling_price
                    discount_percentage = request.session.get('discount_percentage')
                    if discount_percentage:
                        coupon_discount = decimal.Decimal(amount) * decimal.Decimal(discount_percentage) / decimal.Decimal(100)
                        amount -= coupon_discount
                    new_order_item = OrderItem.objects.create(id=unique_order_id,
                                             order=order,
                                            product=cart_item.product,
                                            address=address_obj,
                                            quantity=cart_item.quantity,
                                            payment_method = payment_method,
                                            amount= float(amount))
                    if payment_method == 'online':
                        new_order_item.is_paid = True
                        new_order_item.razor_pay_id = razorpay_payment_id
                        new_order_item.save()
                    product = cart_item.product
                    product.stock -= cart_item.quantity
                    product.save()

                # clear the cart after successful checkout
                cart_items.delete()
                cart.delete()
                if 'discount_percentage' in request.session:
                    del request.session['discount_percentage']
                if 'applied_coupon_code' in request.session:
                    del request.session['applied_coupon_code']

            # Redirect to the order success page or any other page
            return redirect('order_success')  # Replace 'order_success' with your actual URL name
        
        except Exception as e:
            print(e)
            # Handle any other exceptions, such as database errors
            error_message = "An error occurred while processing your order. Please try again later."
            context = {'cart': cart, 'cart_items': cart_items, 'address': address, 'error_message': error_message }
            return render(request, 'checkout.html')
    context = {
        'cart': cart,
        'cart_items': cart_items, 
        'address': address , 
        'coupons':coupons,
        'discount_percentage': request.session.get('discount_percentage'),
        'coupon_code' : request.session.get('applied_coupon_code') }

    return render(request, 'checkout.html', context)
@login_required(login_url='signin')
def order_success(request):
    return render(request,'order_success.html')
@login_required(login_url='admin_login')
def list_orders(request):
    orders = OrderItem.objects.annotate(
    custom_order=Case(
        When(order_status=0, then=Value(0)),
        When(order_status=1, then=Value(0)),
        default=Value(1),
        output_field=IntegerField(),
    )
).order_by('custom_order', '-order_status')
    context = {'orders':orders}
    return render(request, 'list-orders.html', context)
def change_order_status(request, pk):
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
        if status == 3 and order.payment_method == 'cod':
            order.is_paid = True
        order.save()
        #update the stock if order is cancelled by seller
        if status == -2:
            product = order.product
            product.stock += order.quantity
            product.save()
    # Redirect to the list_orders view after processing
    return redirect(request.META.get('HTTP_REFERER', '/'))
@login_required(login_url='signin')
def my_orders(request):
    user = request.user
    orders = OrderItem.objects.filter(order__owner = user).order_by('-created_at')
    context = {'orders': orders}
    return render(request, 'my-order.html', context)
@login_required(login_url='signin')
def order_details(request,pk):
    order = OrderItem.objects.get(pk = pk)
    context = {'order':order}
    return render(request, 'order-details.html', context)
@transaction.atomic
def cancel_order(request, pk):
    try:
        order = OrderItem.objects.select_for_update().get(pk=pk)  # Lock the selected row for update
        order.order_status = -1
        order.save()

        # Update the stock if the order is cancelled
        product = order.product
        product.stock += order.quantity
        product.save()
        if order.is_paid == True:
            wallet = Wallet.objects.select_for_update().get(user=request.user)  # Lock the selected row for update
            wallet.balance += order.amount
            wallet.save()
    except (OrderItem.DoesNotExist, Wallet.DoesNotExist) as e:
        # Handle the case where OrderItem or Wallet does not exist
        # You might want to log the error or return an appropriate response
        return HttpResponseServerError("An error occurred: {}".format(str(e)))
    # Redirect to the order details page after canceling the order
    return redirect('order_details', pk=pk)
def delivery_list(request):
    orders = OrderItem.objects.filter(order_status = 2) 
    context = {'orders':orders}
    return render(request, 'delivery-list.html', context)
def return_order(request,pk):
    order = OrderItem.objects.get(pk = pk)
    if request.POST:
        user = request.user
        product = order.product
        amount = order.amount
        address = order.address
        reason = request.POST.get('reason')
        return_obj = ReturnOrder.objects.create(user=user,product=product,amount_to_refund=amount,reason=reason,address=address, order = order)
        order.order_status = 4
        order.save()
        return redirect('order_details', pk=pk)
    context = {'order':order}
    return render(request, 'return-order.html', context)
def return_list(request):
    return_orders = ReturnOrder.objects.all().order_by('return_status')
    context = {'return_orders':return_orders} 
    return render(request,'return-list.html', context)
@transaction.atomic
def change_return_status(request, pk):
    try:
        return_request_item = ReturnOrder.objects.select_for_update().get(pk=pk) # Lock the selected row for update
        return_request_item.return_status = 2
        return_request_item.save()

        order = return_request_item.order
        order.order_status = 5
        order.save()

        product = return_request_item.product
        product.stock += order.quantity
        product.save() 

        wallet = Wallet.objects.select_for_update().get(user=return_request_item.user) # Lock the selected row for update
        wallet.balance += order.amount
        wallet.save()
    except (ReturnOrder.DoesNotExist, Wallet.DoesNotExist) as e:
        # Handle the case where ReturnOrder or Wallet does not exist
        # You might want to log the error or return an appropriate response
        return HttpResponseServerError("An error occurred: {}".format(str(e)))

    return redirect('return_list')
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {'wishlist_items': wishlist_items}
    return render(request,'wishlist.html', context)

@csrf_exempt
def add_to_wishlist(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Assuming you have some way to identify the current user
        user = request.user
        # Get the product ID from the AJAX request
        product_id = request.POST.get('product_id')
        product = ProductVariant.objects.get(pk=product_id) 
        wishlist_item = Wishlist.objects.create(user=request.user, product=product)
        return JsonResponse({'message': 'Product added to wishlist'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
def remove_from_wishlist(request,pk):
    wishlist_item = Wishlist.objects.get(pk=pk)
    wishlist_item.delete()
    return redirect('wishlist')
def payment_failure(request):
    return render(request,'payment_failure.html')












        







