from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart, name= "cart"),
    path('add_to_cart/', views.add_to_cart, name= "add_to_cart"),
    path('detele_cart_item/<pk>/', views.delete_cart_item, name= "delete_cart_item"),
    path('add_cart_item_quantity/<pk>/', views.add_cart_item_quantity, name= "add_cart_item_quantity"),
    path('sub_cart_item_quantity/<pk>/', views.sub_cart_item_quantity, name= "sub_cart_item_quantity"),
    path('checkout/', views.checkout, name= "checkout"),
    path('order_success/', views.order_success, name= "order_success"),
    path('list_orders/', views.list_orders, name= "list_orders"),
    path('order_cancel_by_seller/<pk>/', views.order_cancel_by_seller, name= "order_cancel_by_seller"),
    path('my_orders/', views.my_orders, name= "my_orders"),
    path('order_details/<pk>/', views.order_details, name= "order_details"),
    path('cancel_order/<pk>/', views.cancel_order, name= "cancel_order"),

    ]

