from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    is_listed = models.BooleanField(default = True) 
    def __str__(self):
        return self.name
    
class Brand(models.Model):
    brand = models.CharField(max_length=50)
    is_listed = models.BooleanField( default = True)
    def __str__(self):
        return self.brand
class ProcessorBrand(models.Model):
    processor_brand_name = models.CharField(max_length=50)
    is_listed = models.BooleanField( default = True)
    def __str__(self):
        return self.processor_brand_name
