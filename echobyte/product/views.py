from django.shortcuts import render


# Create your views here.
def all_products(request):
    return render(request, 'all_products.html')
