from django.contrib import admin
from .models import Brand, ProcessorBrand

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass

@admin.register(ProcessorBrand)
class ProcessorBrandAdmin(admin.ModelAdmin):
    pass
