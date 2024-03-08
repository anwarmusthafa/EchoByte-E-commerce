from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart,CartItems,Order,OrderItem, ReturnOrder
from customer.models import Address,Wallet
from product.models import ProductVariant
from .models import Cart,CartItems, Wishlist
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseServerError, JsonResponse
from django.contrib import messages
from django.db import transaction
import uuid
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Wishlist
from coupon.models import Coupon
import decimal
from django.db.models import Case, When, Value, IntegerField
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from app_admin.decorators import custom_user_passes_test
from decimal import Decimal


# Create your views here.
@login_required(login_url='signin')
def cart(request):
    user = request.user
    try:
        cart_items = CartItems.objects.filter(
        cart__owner=user,
        ).exclude(
        Q(product__is_listed=False) | Q(product__product__is_listed=False)
        ).order_by('-created_at')
        cart = Cart.objects.get(owner=user)
        context = {'cart_items': cart_items,'cart':cart}
    except ObjectDoesNotExist:
        context = {'cart_items': None} 
    return render(request, 'cart.html', context)

from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


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
            return JsonResponse('user not authenticated')
        else:
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
        product_stock = cart_item.product.stock
        if cart_item.quantity == product_stock:
            messages.error(request, "Stock is not availabe")
        elif cart_item.quantity >= 4:
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
    cart_items = CartItems.objects.filter(
        cart__owner=user,
        ).exclude(
        Q(product__is_listed=False) | Q(product__product__is_listed=False)
        ).order_by('-created_at')
    address = Address.objects.filter(user=user)
    coupons = Coupon.objects.filter(is_active = True)
    coupon_discount = None

    if request.method == 'POST':
        address_id = request.POST.get('address')
        amount = float(request.POST.get('amount'))
        payment_method = request.POST.get('payment_method')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        discount_amount = request.POST.get('discount_amount', None) 
        if not address_id:
            error_message = "Please select an address."
            context = {'cart': cart, 'cart_items': cart_items, 'address': address, 'error_message': error_message,'coupons':coupons,}
            return render(request, 'checkout.html',context)
        if amount > 1000 and payment_method == 'cod':
            error_message = "Payment above 1000 can't accept in cash on delivery"
            context = {'cart': cart, 'cart_items': cart_items, 'address': address, 'error_message': error_message,'coupons':coupons,}
            return render(request, 'checkout.html',context) 
        try:
            address_obj = Address.objects.get(pk=address_id)
        except Address.DoesNotExist:
            error_message = "The selected address does not exist."
            context = {'cart': cart, 'cart_items': cart_items, 'address': address, 'error_message': error_message,'coupons':coupons,}
            return render(request, 'checkout.html',context)
        
        try:
            # Create the order transactionally
            with transaction.atomic():
                order = Order.objects.create(owner=user, cart=cart, amount=amount, payment_method=payment_method, discount_amount = discount_amount)
                if payment_method == 'online':
                        order.is_paid = True
                        order.razor_pay_id = razorpay_payment_id
                        order.save()
                if payment_method == 'wallet':
                    wallet = Wallet.objects.get(user=user)
                    if amount > wallet.balance:
                        error_message = f"Insufficient funds in your wallet. Your current balance is {wallet.balance}."
                        context = {'cart': cart, 'cart_items': cart_items, 'address': address, 'error_message': error_message,'coupons':coupons, }
                        return render(request, 'checkout.html',context)
                    else:
                        wallet.balance -= Decimal(amount)
                        wallet.save()
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
                                    total_amount = cart_item.product.selling_price * cart_item.quantity,
                                    discount_amount = coupon_discount,
                                    amount= float(amount))
                    if payment_method == 'online':
                        new_order_item.is_paid = True
                        new_order_item.razor_pay_id = razorpay_payment_id
                        new_order_item.save()
                    if payment_method == 'wallet':
                        new_order_item.is_paid = True
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

            return redirect('order_success') 
        
        except Exception as e:
            error_message = "An error occurred while processing your order. Please try again later."
            context = {'cart': cart, 'cart_items': cart_items, 'address': address, 'error_message': error_message,'coupons':coupons, }
            return render(request, 'checkout.html',context)
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

@custom_user_passes_test(lambda u: u.is_staff)
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

@custom_user_passes_test(lambda u: u.is_staff)
def change_order_status(request, pk):
    order = get_object_or_404(OrderItem, pk=pk)
    if request.method == 'POST':
        status = int(request.POST.get('status'))
        order.order_status = status
        if status == 3 and order.payment_method == 'cod':
            order.is_paid = True
        order.save()
        if status == -2:
            product = order.product
            product.stock += order.quantity
            product.save()
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

@login_required(login_url='signin')
@transaction.atomic
def cancel_order(request, pk):
    try:
        order = OrderItem.objects.select_for_update().get(pk=pk)
        order.order_status = -1
        order.save()
        product = order.product
        product.stock += order.quantity
        product.save()
        if order.is_paid == True:
            wallet = Wallet.objects.select_for_update().get(user=request.user)
            wallet.balance += order.amount
            wallet.save()
    except (OrderItem.DoesNotExist, Wallet.DoesNotExist) as e:
        return HttpResponseServerError("An error occurred: {}".format(str(e)))
    return redirect('order_details', pk=pk)


@custom_user_passes_test(lambda u: u.is_staff)
def delivery_list(request):
    orders = OrderItem.objects.filter(order_status = 2) 
    context = {'orders':orders}
    return render(request, 'delivery-list.html', context)

@login_required(login_url='signin')
def return_order(request,pk):
    order = OrderItem.objects.get(pk = pk)
    if request.POST:
        user = request.user
        product = order.product
        amount = order.amount
        address = order.address
        reason = request.POST.get('reason')
        return_obj = ReturnOrder.objects.create(user=user,
        product=product,
        amount_to_refund=amount,
        reason=reason,address=address,
        order = order)
        order.order_status = 4
        order.save()
        return redirect('order_details', pk=pk)
    context = {'order':order}
    return render(request, 'return-order.html', context)

@custom_user_passes_test(lambda u: u.is_staff)
def return_list(request):
    return_orders = ReturnOrder.objects.all().order_by('return_status')
    context = {'return_orders':return_orders} 
    return render(request,'return-list.html', context)

@custom_user_passes_test(lambda u: u.is_staff)
@transaction.atomic
def change_return_status(request, pk):
    try:
        return_request_item = ReturnOrder.objects.select_for_update().get(pk=pk)
        return_request_item.return_status = 2
        return_request_item.save()

        order = return_request_item.order
        order.order_status = 5
        order.save()

        product = return_request_item.product
        product.stock += order.quantity
        product.save() 

        wallet = Wallet.objects.select_for_update().get(user=return_request_item.user)
        wallet.balance += order.amount
        wallet.save()
    except (ReturnOrder.DoesNotExist, Wallet.DoesNotExist) as e:
        return HttpResponseServerError("An error occurred: {}".format(str(e)))
    return redirect('return_list')

@login_required(login_url='signin')
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {'wishlist_items': wishlist_items}
    return render(request,'wishlist.html', context)

@csrf_exempt
@login_required(login_url='signin')
def add_to_wishlist(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        user = request.user
        product_id = request.POST.get('product_id')
        product = ProductVariant.objects.get(pk=product_id) 
        wishlist_item = Wishlist.objects.create(user=request.user, product=product)
        return JsonResponse({'message': 'Product added to wishlist'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required(login_url='signin')
def remove_from_wishlist(request,pk):
    wishlist_item = Wishlist.objects.get(pk=pk)
    wishlist_item.delete()
    return redirect('wishlist')

@login_required(login_url='signin')
def payment_failure(request):
    return render(request,'payment_failure.html')

@login_required(login_url='signin')
def download_invoice(request, pk):
    order_item = get_object_or_404(OrderItem, pk=pk)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order_item.order_id}.pdf"'
    # Create a PDF canvas
    pdf = canvas.Canvas(response, pagesize=letter)
    # Set font
    pdf.setFont("Helvetica-Bold", 14)
    # Draw Tax Invoice heading
    pdf.drawCentredString(300, 750, "Tax Invoice")
    # Set font size and style for company info
    pdf.setFont("Helvetica", 10)
    # Draw Company Name and GST Number
    pdf.drawString(50, 730, "EchoByte")
    pdf.drawString(50, 715, "GSTIN: 33BGHS74151ZM")  # Assuming you have a gst_number field in your Company model
    # Draw Invoice Number
    pdf.drawRightString(550, 730, f"Invoice Number: {order_item.id}")
    # Draw a line under company info
    pdf.line(50, 710, 550, 710)
    # Set font size for order details
    pdf.setFont("Helvetica-Bold", 12)
    # Draw Order ID and Date
    pdf.drawString(50, 690, f"Order ID: {order_item.pk}")
    pdf.drawString(300, 690, f"Date: {order_item.created_at.strftime('%Y-%m-%d')}")  # Assuming created_at is a DateTimeField
    # Draw Shipping Address
    pdf.drawString(50, 670, f"Bill To: {order_item.address.name}")
    pdf.drawString(50, 650, f"Shipping Address: {order_item.address.address}")
    # Draw a line under order details
    pdf.line(50, 630, 550, 630)
    # Set font size for table header
    pdf.setFont("Helvetica-Bold", 10)
    # Draw table headers
    pdf.drawString(50, 610, "Product")
    pdf.drawString(200, 610, "Quantity")
    pdf.drawString(300, 610, "Amount")
    pdf.drawString(400, 610, "Discount")
    pdf.drawString(500, 610, "Total Amount")
    # Draw a line under table header
    pdf.line(50, 600, 550, 600)
    # Set font size for table data
    pdf.setFont("Helvetica", 10)
    # Draw table data
    y = 580
    product_name = f"{order_item.product.product.brand} - {order_item.product.product.title}"
    pdf.drawString(50, y, product_name)
    pdf.drawString(50, y - 15, f"({order_item.product.variant_name})")  # Adding variant name below product name
    pdf.drawString(200, y, str(order_item.quantity))
    pdf.drawString(300, y, str(order_item.total_amount))
    pdf.drawString(400, y, str(order_item.discount_amount))
    pdf.drawString(500, y, str(order_item.amount))
    y -= 35  # Adjusting the y-coordinate for the next line
    # Draw a line under table data
    pdf.line(50, y, 550, y)
    # Draw Total Price
    pdf.drawString(400, y - 20, "Total Amount:")
    pdf.drawString(500, y - 20, str(order_item.amount))  # Assuming this is the total price
    # Set font size and style for company signature
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y - 40, "Thank you for your purchase from EchoByte!")
    # Close the PDF
    pdf.save()
    return response


@login_required(login_url='signin')
@transaction.atomic
def make_payment(request, pk):
    try:
        payment_id = request.GET.get('razorpay_payment_id')
        order = get_object_or_404(OrderItem, pk=pk)
        order.payment_method = 'online'
        order.is_paid = True
        order.razor_pay_id = payment_id
        order.save()
        context = {'order_id': pk}
        return render(request, 'payment_success.html', context)
    except Exception as e:
        # Rollback transaction in case of any exception
        transaction.set_rollback(True)
        return HttpResponseServerError("An error occurred while processing the payment.")

@login_required(login_url='signin')
def make_payment_failure(request,pk):
    context = {'order_id':pk}
    return render(request,'make_payment_failure.html',context)
