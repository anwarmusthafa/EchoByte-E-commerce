from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
@never_cache
def admin_login(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('admin_home')
        else:
            error_message = "Invalid Credentials"
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
