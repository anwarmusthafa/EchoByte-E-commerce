
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *
import random


def genotp():
    return str(random.randint(1000,9999))


@receiver(post_save, sender = Customer)
def send_otp_signal(sender, instance,created, **kwargs):

    if created and instance.is_verified == False:
        send_otp(instance)    
        
        
def send_otp(user):
        otp1 = genotp()
        print(otp1)
        otp1 = int(otp1)
        user.otp = otp1   
        user.save()
        subject = 'Welcome to shopzy this is for otp verification'
        message = f"your otp is: {otp1}"
        from_email = "echobyte24@gmail.com"
        to_email = [user.user.username]
        send_mail(subject,message,from_email,to_email)
     