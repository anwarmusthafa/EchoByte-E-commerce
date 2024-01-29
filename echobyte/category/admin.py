from django.contrib import admin
from .models import Brand,Category

@admin.register(Category)
class CatogoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass

