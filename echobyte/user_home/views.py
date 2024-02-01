from django.shortcuts import render
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def home(request):
    user = request.user
    return render(request, 'index.html',{'user':user})
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')



