from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import user_passes_test
from product.models import ProductVariant
from django.db.models import Q

# Create your views here.
@never_cache

def home(request):
    new_arrivals = ProductVariant.objects.exclude(
    Q(product__delete_status=0) |
    Q(product__is_listed=False) |
    Q(product__category__is_listed=False) |
    Q(is_listed=False)).order_by('product__title', '-product__created_at').distinct('product__title')[:6]

    context = {'new_arrivals':new_arrivals}
    return render(request, 'index.html',context)
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
    
        



