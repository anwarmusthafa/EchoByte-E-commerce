from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name= "home"),
    path('all_products', views.all_products, name= "all_products"),
    path('about', views.about, name= "about"),
    path('contact', views.contact, name= "contact"),
    
]
