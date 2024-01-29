from django.db import models
from django.utils.translation import gettext as _
from category.models import Brand,Category

    
class Product(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICES = ((LIVE, 'Live'), (DELETE, 'Delete'))
    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    sub_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank = True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null = True,related_name='products')
    display = models.CharField( max_length=50, null = True, blank = True)
    front_camera = models.CharField(max_length=50, null= True, blank = True)
    back_camera = models.CharField(max_length=50, null = True, blank = True)
    processor = models.CharField(max_length=50, null = True)
    priority = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    battery_capacity = models.CharField( max_length=50, null = True)
    is_listed = models.BooleanField(default = True) 
    def __str__(self):
        return self.title
    def variant_count(self):
        return self.variants.count()
class ProductVariant(models.Model):
     RAM_CHOICES = (
         ('512MB', '512MB'),
         ('1GB', '1GB'),
         ('2GB', '2GB'),
        ('4GB', '4GB'),
        ('6GB', '6GB'),
        ('8GB', '8GB'),
        ('12GB', '12GB'),
        ('16GB', '16GB'),
        ('32GB', '32GB'),
     )
     STORAGE_CHOICES = (
         ('8GB', '8GB'),
         ('32GB', '32GB'),
         ('64GB', '64GB'),
         ('16GB', '16GB'),
         ('32GB', '32GB'),
        ('64GB', '64GB'),
        ('128GB', '128GB'),
        ('256GB', '256GB'),
        ('512GB', '512GB'),
        ('1TB', '1TB'),
        ('2TB', '2TB'),
     )
     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
     variant_name = models.CharField(_("Variant Name"), max_length=50)
     ram = models.CharField(_("RAM"), choices=RAM_CHOICES)
     storage = models.CharField(_("Internal Storage"), choices=STORAGE_CHOICES)
     colour = models.CharField(_("Product Colour"), null = True, blank =True ,max_length=50)
     original_price = models.DecimalField(_("Original Price"), max_digits=10, decimal_places=2)
     selling_price = models.DecimalField(_("Setting Price"), max_digits=10, decimal_places=2)
     stock = models.PositiveIntegerField(_("Stock"), default=0)
     is_listed = models.BooleanField(default = True)
     def __str__(self):
        return f"{self.product.title} - {self.variant_name}"
     def discount_percentage(self):
         discount_percentage = int( ((self.original_price - self.selling_price) / self.original_price) * 100)
         return discount_percentage
     
class ProductImage(models.Model):
    product = models.ForeignKey(Product,verbose_name=_("Product Images"), on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(_("Product Image"), upload_to="product images/", height_field=None, width_field=None, max_length=None , null=True, blank=True)
    image_order = models.PositiveIntegerField(_("Image order"))
    def __str__(self):
        return f"{self.product.title} - Image {self.image_order}"
