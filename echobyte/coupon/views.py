from django.shortcuts import render
from django.shortcuts import redirect, HttpResponse
from django.contrib import messages
from .models import *

# Create your views here
def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon-code')
        try:
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)
            discount_percentage = coupon.discount_percentage
            request.session['discount_percentage'] = discount_percentage
            request.session['applied_coupon_code'] = coupon_code
            messages.success(request, 'Coupon applied successfully!')
        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code. Please try again.')
        return redirect('checkout')
    else:
        return HttpResponse('Method not allowed', status=405)
    
def remove_coupon(request):
    if 'discount_percentage' in request.session:
        del request.session['discount_percentage']
    if 'applied_coupon_code' in request.session:
        del request.session['applied_coupon_code']
    return redirect('checkout')
def clear_session(request):
    # Clear all session data
    request.session.flush()
    return HttpResponse("Session cleared successfully!")





