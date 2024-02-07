from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart, name= "cart"),
    path('add_to_cart/', views.add_to_cart, name= "add_to_cart"),
    path('detele_cart_item/<pk>/', views.delete_cart_item, name= "delete_cart_item"),
    path('add_cart_item_quantity/<pk>/', views.add_cart_item_quantity, name= "add_cart_item_quantity"),
    ]

