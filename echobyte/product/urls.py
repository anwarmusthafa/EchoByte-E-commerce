from django.urls import path
from . import views

urlpatterns = [
    path('all_products/', views.all_products, name= "all_products"),
    path('product_detail/<int:pk>/', views.product_detail, name = "product_detail"),
    path('list_product/', views.list_product, name='list_product'),
    path('product_delete/<pk>/', views.product_delete, name='product_delete'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_variant/', views.add_variant, name='add_variant'),
    path('list_variants/', views.list_variants, name='list_variants'),
    path('variant_block/<pk>/', views.variant_block, name='variant_block'),
    path('edit_product/<pk>/', views.edit_product, name='edit_product'),
    path('edit_variant/<pk>/', views.edit_variant, name='edit_variant'),
] 

