from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from customer.models import Customer
from product.models import Product,ProductVariant
@never_cache
def admin_login(request):
    error_message = None
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user and user.is_staff:
                login(request, user)
                return redirect('admin_home')
            else:
                raise ValueError("Invalid Credentials")
    except Exception as e:
        # Handle specific exception types if needed
        error_message = str(e)
    context = {'error_message': error_message}
    return render(request, 'admin_login.html', context)

@never_cache
@login_required(login_url='admin_login')
def admin_home(request):
    return render(request, 'admin_home.html')

@never_cache
@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

def customers_list(request):
     customers = User.objects.exclude(pk = 1)
     context = {'customers': customers}
     return render(request, 'customers_list.html', context)
def delete_status(request, pk):
    if request.POST:
        delete_status = int(request.POST.get('delete_status'))
        print(delete_status)
        user = get_object_or_404(Customer,user_id=pk)
        if delete_status == 0:
            user.delete_status = 0
        else:
            user.delete_status = 1
        user.save()
    return redirect('customers_list')
def list_product(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request,'list_product.html', context)
def product_delete(request,pk):
    if request.POST:
        delete_status = int(request.POST.get('delete_status'))
        print(delete_status)
        product = get_object_or_404(Product,pk=pk)
        if delete_status == 0:
            product.delete_status = 0
        else:
            product.delete_status = 1
        product.save()
    return redirect('list_product')



