from django.shortcuts import render
from django.shortcuts import redirect, HttpResponse
from django.contrib import messages
from .models import *
from datetime import date

# Create your views here

def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon-code')
        try:
            today = date.today()
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)
            
            if coupon.valid_from and coupon.valid_to:
                if today < coupon.valid_from or today > coupon.valid_to:
                    messages.error(request, 'Coupon is not valid yet or has expired.')
                    return redirect('checkout')

            discount_percentage = coupon.discount_percentage
            request.session['discount_percentage'] = discount_percentage
            request.session['applied_coupon_code'] = coupon_code
            messages.success(request, 'Coupon applied successfully!')
        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code. Please try again.')
        except Coupon.MultipleObjectsReturned:
            messages.error(request, 'Multiple coupons found with the same code. Please contact support.')
        return redirect('checkout')
    else:
        return HttpResponse('Method not allowed', status=405)

    
def remove_coupon(request):
    if 'discount_percentage' in request.session:
        del request.session['discount_percentage']
    if 'applied_coupon_code' in request.session:
        del request.session['applied_coupon_code']
    return redirect('checkout')
def coupon_list(request):
    coupons = Coupon.objects.all()
    context = {'coupons':coupons}
    return render(request,'coupon_list.html', context)
def add_coupon(request):
    if request.POST:
        title = request.POST.get('title')
        code = request.POST.get('code')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        discount_percentage = request.POST.get('discount_percentage')
        coupon = Coupon.objects.create(title=title,code=code,valid_from=valid_from,discount_percentage=discount_percentage)
        return redirect('coupon_list') 
    return render(request, 'add_coupon.html')





