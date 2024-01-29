from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.categories, name= "categories"),
    path('brands/', views.brands, name= "brands"),
    path('add_category/', views.add_category, name= "add_category"),
    path('add_category/<pk>/', views.edit_category, name= "edit_category"),
]
