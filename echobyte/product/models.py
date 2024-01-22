from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [('mobile','Mobile'), ('laptop','laptop'),('all','All')]
    title = models.CharField(max_length=50)
    description = models.TextField()
    category = models.CharField(max_length= 10, choices = CATEGORY_CHOICES, default = 'all')
    

