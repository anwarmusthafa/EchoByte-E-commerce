from django.db import models

# Create your models here.
class Banner(models.Model):
    banner_name = models.CharField(max_length=50)
    banner_heading = models.CharField(max_length=50)
    banner_order = models.PositiveIntegerField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    expiry_date = models.DateField( auto_now=False, auto_now_add=False)
    is_listed = models.BooleanField(default = True)
    banner_image = models.ImageField(upload_to="banner images/", height_field=None, width_field=None, max_length=None,null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    
