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
    path('change_order_status/<pk>/', views.change_order_status, name= "change_order_status"),
    path('my_orders/', views.my_orders, name= "my_orders"),
    path('order_details/<pk>/', views.order_details, name= "order_details"),
    path('cancel_order/<pk>/', views.cancel_order, name= "cancel_order"),
    path('delivery_list/', views.delivery_list, name= "delivery_list"),
    path('return_order/<pk>/', views.return_order, name= "return_order"),
    path('return_list/', views.return_list, name= "return_list"),
    path('change_return_status/<pk>/', views.change_return_status, name= "change_return_status"),
    path('add_to_wishlist/', views.add_to_wishlist, name= "add_to_wishlist"),
    path('wishlist/', views.wishlist, name= "wishlist"),
    path('remove_from_wishlist/<pk>/', views.remove_from_wishlist, name= "remove_from_wishlist"),
    path('payment_failure/', views.payment_failure, name= "payment_failure"),
    path('download_invoice/<pk>/', views.download_invoice, name= "download_invoice"),
    
    

    ]

