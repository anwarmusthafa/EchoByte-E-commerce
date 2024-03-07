from django.shortcuts import render
from django.shortcuts import redirect, HttpResponse
from django.contrib import messages
from .models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from app_admin.decorators import custom_user_passes_test

@login_required(login_url='signin')
def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon-code')
        try:
            today = timezone.now().date()
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)
            if coupon.valid_from or coupon.valid_to:
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

@login_required(login_url='signin')   
def remove_coupon(request):
    if 'discount_percentage' in request.session:
        del request.session['discount_percentage']
    if 'applied_coupon_code' in request.session:
        del request.session['applied_coupon_code']
    return redirect('checkout')

@custom_user_passes_test(lambda u: u.is_staff)
def coupon_list(request):
    coupons = Coupon.objects.all()
    context = {'coupons':coupons}
    return render(request,'coupon_list.html', context)

@custom_user_passes_test(lambda u: u.is_staff)
def add_coupon(request):
    if request.POST:
        title = request.POST.get('title')
        code = request.POST.get('code')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        discount_percentage = request.POST.get('discount_percentage')
        coupon = Coupon.objects.create(title=title,code=code,valid_from=valid_from,valid_to = valid_to,discount_percentage=discount_percentage)
        return redirect('coupon_list') 
    return render(request, 'add_coupon.html')

@custom_user_passes_test(lambda u: u.is_staff)
def delete_coupon(request,pk):
    coupon = Coupon.objects.get(pk=pk)
    coupon.delete()
    return redirect('coupon_list')

def category_offer(request):
    category_offers = CategoryOffer.objects.all()
    context = {'category_offers':category_offers}
    return render(request,'category_offer.html',context)
def add_category_offer(request):
    if request.POST:
        title = request.POST.get('title')
        category_id = int(request.POST.get('category'))
        offer_percentage = request.POST.get('offer_percentage')
        category_obj = Category.objects.get(pk = category_id) 
        category_offer_obj = CategoryOffer.objects.create(title=title,category = category_obj, offer_percentage = offer_percentage)
        return redirect('category_offer')
    categories = Category.objects.all()
    context = {'categories': categories}
    
    return render(request,'add_category_offer.html',context)

def delete_category_offer(request,pk):
    category_offer = CategoryOffer.objects.get(pk = pk)
    category_offer.delete()
    return redirect('category_offer')





