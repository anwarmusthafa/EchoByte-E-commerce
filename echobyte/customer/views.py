from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from .models import Customer

@never_cache
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to the home page if the user is already authenticated

    error_message = None
    if request.method == 'POST':
        login_identifier = request.POST.get('login_identifier')
        password = request.POST.get('password')

        # Debugging output
        print(f"Attempting to authenticate with: {login_identifier} / {password}")

        user = authenticate(request, username=login_identifier, password=password)
        if user and not user.is_staff:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid Credentials"

    context = {"error_message": error_message}
    return render(request, 'signin.html', context)

@never_cache
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to the home page if the user is already authenticated

    last_typed_values = request.session.pop('signup_last_typed_values', {})
    error_message = request.session.pop('signup_error_message', None)
    success_message = None

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')

        last_typed_values = {
            'name': name,
            'email': email,
            'phone': phone,
        }

        if password1 != password2:
            request.session['signup_last_typed_values'] = last_typed_values
            request.session['signup_error_message'] = 'Passwords do not match'
            return redirect('signup')

        try:
            # Check if the email is already in use
            User.objects.get(username=email)
            request.session['signup_last_typed_values'] = last_typed_values
            request.session['signup_error_message'] = 'Email address is already in use'
            return redirect('signup')
        except User.DoesNotExist:
            # If the user does not exist, create a new user and log them in
            user = User.objects.create_user(username=email, password=password1)
            Customer.objects.create(user=user, name=name, phone=phone)
            success_message = 'Registration is successful'
        except Exception as e:
            request.session['signup_last_typed_values'] = last_typed_values
            request.session['signup_error_message'] = f'Error during signup: {str(e)}'
            return redirect('signup')

    context = {
        'last_typed_values': last_typed_values,
        'error_message': error_message,
        'success_message': success_message
    }
    print(f"Success message: {success_message}")
    print(f"Error message: {error_message}")
    return render(request, 'signup.html', context)

@never_cache
@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('signin')
