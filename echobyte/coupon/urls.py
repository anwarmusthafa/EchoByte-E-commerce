from django.urls import path
from . import views

urlpatterns = [
    path('apply_coupon/', views.apply_coupon, name= "apply_coupon"),
    path('remove_coupon/', views.remove_coupon, name= "remove_coupon"),
    path('clear-session/', views.clear_session, name='clear_session'),
    ]