from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Customer

def signin(request):
    
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')  # Fix: Corrected the key to 'password2'
        phone = request.POST.get('phone')

        if password1 == password2:
            # Fix: Use 'create_user' instead of 'create'
            user = User.objects.create(username=username, email=email, password=password1)
            # Assuming you want to log the user in immediately after signup
            customer = Customer.objects.create(user = user, phone = phone)
            return redirect('home')  # Change 'home' to your desired redirect path
        else:
            # Handle password mismatch error
            return render(request, 'signup.html', {'error_message': 'Passwords do not match'})

    return render(request, 'signup.html')
