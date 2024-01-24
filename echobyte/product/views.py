from django.shortcuts import render
from .models import ProductVariant, ProductImage


# Create your views here.
def all_products(request):
    variants = ProductVariant.objects.exclude(product__delete_status = 0)
    context = {'variants' : variants}
    return render(request, 'all_products.html', context)
def product_detail(request, pk):
    product = ProductVariant.objects.get(id = pk)
    product_images = ProductImage.objects.filter(product= product.product)
    context = {'product':product, 'product_images' : product_images}
    return render(request, 'product-detail.html', context)