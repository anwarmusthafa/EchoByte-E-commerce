from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.categories, name= "categories"),
    path('brands/', views.brands, name= "brands"),
    path('add_category/', views.add_category, name= "add_category"),
    path('edit_category/<pk>/', views.edit_category, name= "edit_category"),
    path('add_brand/', views.add_brand, name= "add_brand"),
    path('edit_brand/<pk>/', views.edit_brand, name= "edit_brand"),
    path('block_category/<pk>/', views.block_category, name= "block_category"),
    path('block_brand/<pk>/', views.block_brand, name= "block_brand"),
]
