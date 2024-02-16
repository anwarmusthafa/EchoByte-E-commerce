from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICES = ((LIVE, 'Live'), (DELETE, 'Delete'))
    name = models.CharField(max_length=50, null = True)
    phone = models.CharField(max_length=50, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    otp = models.IntegerField(null = True, blank = True)
    is_verified = models.BooleanField(default = False)
    def __str__(self):
        return self.name
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', null = True)  # Added related_name
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    address = models.TextField()
    pincode = models.PositiveIntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    def __str__(self):
        return self.user.username+ "'s address"
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('suspended', 'Suspended'), ('closed', 'Closed')], default='active')

    def __str__(self):
        return f"{self.user.customer.name}'s Wallet"

    
    
