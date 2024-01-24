from django.urls import path
from . import views

urlpatterns = [
    path('admin_home/', views.admin_home, name= "admin_home"),
    path('admin_login/', views.admin_login, name= "admin_login"),
    path('admin_logout/', views.admin_logout, name= "admin_logout"),
    path('customers_list/', views.customers_list, name= "customers_list"),
    path('delete_status/<pk>/', views.delete_status, name='delete_status'),
    path('list_product/', views.list_product, name='list_product'),
    path('product_delete/<pk>/', views.product_delete, name='product_delete')
] 
