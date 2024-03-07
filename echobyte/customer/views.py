from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from .models import Customer, Address, Wallet
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from .signals import send_otp
from django.http import HttpResponseServerError
from order.models import *
from django.contrib import messages
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
import random
import re


@never_cache
def signin(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('home')
    
    error_message = None
    success_message = request.GET.get('success_message', None)
    
    if request.method == 'POST':
        login_identifier = request.POST.get('login_identifier')
        password = request.POST.get('password')
        user = authenticate(request, username=login_identifier, password=password)
        
        if user:
            if user.is_superuser:
                error_message = "Superusers are not allowed to sign in."
            elif not user.is_staff:
                if user.customer.is_verified:
                    if user.customer.delete_status == 0:
                        error_message = "You are blocked by Admin"
                    else:
                        login(request, user)
                        return redirect('home')
                else:
                    # Use messages framework to display error message
                    messages.error(request, "Verify your email")
                    send_otp(user.customer)
                    return redirect('otp_verification', pk=user.customer.pk)
            else:
                error_message = "Invalid Credentials"  # This line is for non-staff users
    
        else:
            error_message = "Invalid Credentials"  # This line is for when user is None (authentication failed)
    
    context = {"error_message": error_message, "success_message": success_message}
    return render(request, 'signin.html', context)

@never_cache
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

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
            with transaction.atomic():
                User.objects.get(username=email)
                request.session['signup_last_typed_values'] = last_typed_values
                request.session['signup_error_message'] = 'Email address is already in use'
                return redirect('signup')
        except User.DoesNotExist:
            try:
                with transaction.atomic():
                    user = User.objects.create_user(username=email, password=password1)
                    user1 = Customer.objects.create(user=user, name=name, phone=phone)
                    return redirect('otp_verification', user1.id)
            except Exception as e:
                request.session['signup_last_typed_values'] = last_typed_values
                request.session['signup_error_message'] = f'Error during signup: {str(e)}'
                return redirect('signup')

    context = {
        'last_typed_values': last_typed_values,
        'error_message': error_message,
        'success_message': success_message
    }
    return render(request, 'signup.html', context)

@never_cache
@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('signin')

def otp_verification(request, pk):
    success_message = None
    try: 
        if request.method == 'POST':
            user_otp = request.POST['otp']
            tb_user = get_object_or_404(Customer, pk=pk)
            db_otp = tb_user.otp 
            if  user_otp == str(db_otp):
                if tb_user.is_verified:
                    return render(request, 'signin',{'pk':pk})
                else:
                    tb_user.is_verified = True
                    tb_user.save()
                    success_message = "Registration Successfull Please Login Now"
                    return render(request, 'signin.html', {'pk': pk, 'success_message': success_message})
            else:
                    messages.error(request,"Invalid otp Try again!")
                    return redirect('otp_verification',pk = pk,)
    except Exception as e:
        print(e)
    context={ 'pk':pk,
             'success_message' : success_message}
    return render(request, 'otp_verification.html', context)

@login_required(login_url='signin')
def profile(request):
    user = request.user
    customer = Customer.objects.get(user__username = user)
    context = {'customer':customer}
    return render(request,'profile.html', context)

@login_required(login_url='signin')
def edit_profile(request):
    user = request.user
    customer = Customer.objects.get(user__username=user)
    if request.POST:
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        customer.name = name
        customer.phone = phone
        customer.save()
        return redirect('profile')
    context = {'customer':customer} 
    return render(request, 'edit-profile.html', context)

@login_required(login_url='signin')
def address(request):
    address = Address.objects.filter(user = request.user)
    context = {'address':address}
    return render(request, 'address.html', context )

@login_required(login_url='signin')
def add_address(request):
    if request.POST:
        try:
            user = request.user 
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            state = request.POST.get('state')
            city = request.POST.get('town')
            pincode = request.POST.get('pincode')
            source = request.POST.get('source', None)

           
            try:
                address_obj = Address.objects.create(
                    user=user,
                    name=name,
                    phone=phone,
                    address=address,
                    pincode=pincode,
                    city=city,
                    state=state
                )
                if source == 'checkout':
                    return redirect('checkout')
                else:
                    return redirect('address')
            except Exception as e:
                return HttpResponseServerError("Failed to create address: {}".format(str(e)))
        except Exception as e:
            return HttpResponseServerError("An error occurred: {}".format(str(e)))
    return render(request, 'add-address.html')
@login_required(login_url='signin')
def delete_address(requrest,pk):
    address = Address.objects.get(pk=pk)
    address.delete()
    return redirect('address')

def edit_address(request,pk):
    address = Address.objects.get(pk =pk)
    existing_state = address.state
    state_options = ['Kerala', 'Tamil Nadu', 'Karnataka']
    filtered_options = [option for option in state_options if option != existing_state]
    if request.POST: 
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            given_address = request.POST.get('address')
            state = request.POST.get('state')
            city = request.POST.get('town')
            pincode = request.POST.get('pincode')
            address.name = name
            address.phone = phone
            address.address = given_address
            address.state = state
            address.city = city
            address.pincode = pincode
            address.save()
            return redirect('address')

    context = {'address':address, 'filtered_options':filtered_options}
    return render(request,'edit_address.html',context)

@login_required(login_url='signin')
def wallet(request):
    wallet = Wallet.objects.get(user = request.user)
    context = {
        'wallet': wallet
    }
    return render(request, 'wallet.html', context)


def validate_password(password):
    # Check if password length is at least 8 characters
    if len(password) < 6:
        return False
    
    # Check if password contains at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False
    
    # Check if password contains at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False
    
    # Check if password contains at least one digit
    if not re.search(r'\d', password):
        return False
    
    # Check if password contains at least one special character
    if not re.search(r'[!@#$%^&*()\-_=+{};:,<.>]', password):
        return False
    
    return True

def change_password(request):
    error_message = None
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password_1 = request.POST.get('new_password_1')
        new_password_2 = request.POST.get('new_password_2')
        if new_password_1 != new_password_2:
            error_message = "Passwords do not match"
            return render(request, 'change_password.html', {'error_message': error_message}) 
        user = request.user
        if not authenticate(username=user.username, password=current_password):
            error_message = "Current password is incorrect"
            return render(request, 'change_password.html', {'error_message': error_message})
        # Validate new password complexity
        if not validate_password(new_password_1):
            error_message = "Password Should have One upper case, One lowercase, One digit, One Symbol and minimum lenth 6"
            return render(request, 'change_password.html', {'error_message': error_message})
        # Now, update the user's password
        hashed_password = make_password(new_password_1)
        user.password = hashed_password
        user.save()
        success_message = "Password has been successfully updated"
        return render(request, 'change_password.html', {'success_message': success_message})
        
    return render(request, 'change_password.html', {'error_message': error_message})

def genotp():
    return str(random.randint(1000,9999))

def forgot_password(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            user = User.objects.get(username=email)
            customer = user.customer
            def send_otp(email):
                otp1 = genotp()
                print(otp1)
                otp1 = int(otp1)
                customer.otp = otp1
                customer.save()
                subject = 'EchoByte otp verification'
                message = f"Forgot password verification otp is: {otp1}"
                from_email = "echobyte24@gmail.com"
                to_email = [email]
                send_mail(subject, message, from_email, to_email)
            send_otp(email)
            return redirect('otp_verification_forgot_password', user.pk)
        
        except User.DoesNotExist:
            # Handle case when user does not exist
            return render(request, 'forgot_password.html', {'error': 'This user is does not exist'})
        
        except Exception as e:
            # Handle other exceptions
            return render(request, 'forgot_password.html', {'error': str(e)})
    return render(request, 'forgot_password.html')
def otp_verification_forgot_password(request,pk):
    error_message = None
    if request.POST:
        otp = int(request.POST.get('otp'))
        user = Customer.objects.get(user__pk = pk)
        print(user.otp)
        user_id = user.user.pk 
        if otp == user.otp:
            return redirect('reset_password',user_id)
        else:
            error_message  = "Otp is incorrect"
    return render(request,'otp_verification_forgot_password.html',{'error_message':error_message})
def reset_password(request, pk):
    if request.method == 'POST':
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        if password_1 != password_2:
            error_message = "Passwords do not match"
            return render(request, 'reset_password.html', {'error_message': error_message})
        # Validate new password complexity
        if not validate_password(password_1):
            error_message = "Password should have one upper case, one lowercase, one digit, one symbol and minimum length 6"
            return render(request, 'reset_password.html', {'error_message': error_message})
        # Now, update the user's password
        user = User.objects.get(pk=pk)
        hashed_password = make_password(password_1)
        user.password = hashed_password
        user.save()
        # Redirect to sign-in page with success message
        success_message = "Password has been successfully updated. Please sign in."
        return redirect(reverse('signin') + '?success_message=' + success_message)
    return render(request, 'reset_password.html')
    
        
