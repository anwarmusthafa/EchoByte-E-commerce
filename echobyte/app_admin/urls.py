from django.urls import path
from . import views

urlpatterns = [
    path('admin_home/', views.admin_home, name= "admin_home"),
    path('admin_login/', views.admin_login, name= "admin_login"),
    path('admin_logout/', views.admin_logout, name= "admin_logout"),
    path('customers_list/', views.customers_list, name= "customers_list"),
    path('delete_status/<pk>/', views.delete_status, name='delete_status'),
    path('list_product/', views.list_product, name='list_product'),
    path('product_delete/<pk>/', views.product_delete, name='product_delete'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_variant/', views.add_variant, name='add_variant'),
    path('list_variants/', views.list_variants, name='list_variants'),
    path('variant_block/<pk>/', views.variant_block, name='variant_block'),
] 
