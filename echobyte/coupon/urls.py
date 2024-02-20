from django.urls import path
from . import views

urlpatterns = [
    path('apply_coupon/', views.apply_coupon, name= "apply_coupon"),
    path('remove_coupon/', views.remove_coupon, name= "remove_coupon"),
    path('coupon_list/', views.coupon_list, name= "coupon_list"),
    path('add_coupon/', views.add_coupon, name= "add_coupon"),

    ]