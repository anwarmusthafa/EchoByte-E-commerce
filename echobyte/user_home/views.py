from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
@never_cache

def home(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')



