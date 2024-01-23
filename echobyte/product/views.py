from django.shortcuts import render
from .models import Product,ProductVariant


# Create your views here.
def all_products(request):
    variants = ProductVariant.objects.all()
    for variant in variants:
        print(variant.product.images.first())
    context = {'variants' : variants}
    return render(request, 'all_products.html', context)
