from django.urls import path
from . import views

urlpatterns = [
    path('appy_coupon/', views.apply_coupon, name= "apply_coupon"),
    path('clear-session/', views.clear_session, name='clear_session'),
    ]