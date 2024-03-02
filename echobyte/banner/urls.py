from django.urls import path
from . import views

urlpatterns = [
    path('banners/', views.banners, name="banners"),
    path('change_banner_status/<pk>', views.change_banner_status, name="change_banner_status"),
    path('add_banner/', views.add_banner, name="add_banner"),
    path('delete_banner/<pk>', views.delete_banner, name="delete_banner"),
    
]
