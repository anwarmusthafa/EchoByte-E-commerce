from django.db import models
from category.models import Category
from django.core.validators import MinValueValidator

# Create your models here.
class Coupon(models.Model):
    title = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    valid_from = models.DateField(null = True , blank = True)
    valid_to = models.DateField( null = True , blank = True)
    discount_percentage = models.FloatField()
    is_active = models.BooleanField(default = True)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.title
class CategoryOffer(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    offer_percentage = models.FloatField(validators=[MinValueValidator(0.0)])
    is_listed = models.BooleanField(default = True)



    