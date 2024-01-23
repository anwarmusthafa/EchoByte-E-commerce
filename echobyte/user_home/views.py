from django.shortcuts import render
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def home(request):
    return render(request, 'index.html')
def all_products(request):
    return render(request, 'all_products.html')
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')



