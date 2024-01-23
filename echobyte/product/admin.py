from django.contrib import admin
from .models import Product, ProductVariant, ProductImage, Brand

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass
