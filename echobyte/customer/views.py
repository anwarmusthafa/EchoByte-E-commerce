from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import login
from .models import Customer

def signin(request):
    error_message = None
    if request.POST:
        login_identifier = request.POST.get('login_identifier')
        password = request.POST.get('password')
        user = authenticate(request, username = login_identifier , password = password)
        if user and not user.is_staff:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid Credentials"
    context = { "error_message" : error_message}
    return render(request,'signin.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Customer
def signup(request):
    # Get the last typed values from the session, if any
    last_typed_values = request.session.get('signup_last_typed_values', {})
    # Clear the last typed values from the session
    request.session.pop('signup_last_typed_values', None)

    # Get the error message from the session, if any
    error_message = request.session.get('signup_error_message', None)
    # Clear the error message from the session
    request.session.pop('signup_error_message', None)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Store the last typed values in the session
        last_typed_values = {
            'name': name,
            'email': email,
            'phone': request.POST.get('phone'),
        }

        # Check if passwords match
        if password1 != password2:
            request.session['signup_last_typed_values'] = last_typed_values
            request.session['signup_error_message'] = 'Passwords do not match'
            return redirect('signup')

        try:
            # Check if the email is already in use
            existing_user = User.objects.get(username=email)
            request.session['signup_last_typed_values'] = last_typed_values
            request.session['signup_error_message'] = 'Email address is already in use'
            return redirect('signup')
        except User.DoesNotExist:
            # If the user does not exist, create a new user and log them in
            user = User.objects.create_user(username=email, password=password1)
            customer = Customer.objects.create(user=user, name=name, phone=request.POST.get('phone'))
            return redirect('home')  # Change 'home' to your desired redirect path
        except Exception as e:
            # Handle other exceptions
            request.session['signup_last_typed_values'] = last_typed_values
            request.session['signup_error_message'] = f'Error during signup: {str(e)}'
            return redirect('signup')

    return render(request, 'signup.html', {'last_typed_values': last_typed_values, 'error_message': error_message})

def signout(request):
    logout(request)
    return redirect('signin')
