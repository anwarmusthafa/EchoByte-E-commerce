from django.db import models
from django.utils.translation import gettext as _
class Brand(models.Model):
    brand = models.CharField(_("brand"), max_length=50)
    is_listed = models.BooleanField(_(""), default = True)
    def __str__(self):
        return self.brand
    

class Product(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICES = ((LIVE, 'Live'), (DELETE, 'Delete'))
    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)
    CATEGORY_CHOICES = [('mobile','Mobile'), ('laptop','laptop'),('all','All')]
    title = models.CharField(max_length=50)
    description = models.TextField()
    category = models.CharField(max_length= 10, choices = CATEGORY_CHOICES, default = 'all')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null = True)
    priority = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
class ProductVariant(models.Model):
     RAM_CHOICES = (
        ('4GB', '4GB'),
        ('6GB', '6GB'),
        ('8GB', '8GB'),
        ('12GB', '12GB'),
        ('16GB', '16GB'),
        ('32GB', '32GB'),
     )
     STORAGE_CHOICES = (
        ('64GB', '64GB'),
        ('128GB', '128GB'),
        ('256GB', '256GB'),
        ('512GB', '512GB'),
        ('1TB', '1TB'),
        ('2TB', '2TB'),
     )
     product = models.ForeignKey(Product, on_delete=models.CASCADE)
     varient_name = models.CharField(_("Variant Name"), max_length=50)
     ram = models.CharField(_("RAM"), choices=RAM_CHOICES)
     storage = models.CharField(_("Internal Storage"), choices=STORAGE_CHOICES)
     colour = models.CharField(_("Product Colour"), max_length=50)
     original_price = models.DecimalField(_("Original Price"), max_digits=10, decimal_places=2)
     selling_price = models.DecimalField(_("Setting Price"), max_digits=10, decimal_places=2)
     stock = models.PositiveIntegerField(_("Stock"), default=0)
     def __str__(self):
        return f"{self.product.title} - {self.varient_name}"
class ProductImage(models.Model):
    product = models.ForeignKey(Product,verbose_name=_("Product Images"), on_delete=models.CASCADE)
    image = models.ImageField(_("Product Image"), upload_to="media/product images", height_field=None, width_field=None, max_length=None)
    image_order = models.PositiveIntegerField(_("Image order"))
    def __str__(self):
        return f"{self.product.title} - Image {self.image_order}"




    

    

