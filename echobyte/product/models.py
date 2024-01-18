# # models.py

# from django.db import models

# class Product(models.Model):
#     title = models.CharField(max_length=50)
#     description = models.TextField()
#     display = models.CharField(max_length=50)
#     category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

# class Category(models.model):
#     name = models.CharField(max_length=50)


# class ProductVariant(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     ram = models.CharField(max_length=20)
#     storage = models.CharField(max_length=20)
#     color = models.CharField(max_length=20)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     category = models.ForeignKey(Category,on_delete=models.CASCADE)
#     priority = models.IntegerField(default = 0)

#     def __str__(self):
#         return f"{self.product.title} - {self.ram} {self.storage} {self.color}"

# class ProductVariant(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     ram = models.CharField(max_length=20)
#     storage = models.CharField(max_length=20)
#     color = models.CharField(max_length=20)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.product.title} - {self.ram} {self.storage} {self.color}"
