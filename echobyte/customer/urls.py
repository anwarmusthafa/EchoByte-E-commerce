from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin, name= "signin"),
    path('signup/', views.signup, name= "signup"),
    path('signout/', views.signout, name= "signout"),
    path('otp_verification/<pk>/', views.otp_verification, name= "otp_verification"),
    path('profile/', views.profile, name= "profile"),
    path('edit_profile/', views.edit_profile, name= "edit_profile"),
    path('address/', views.address, name= "address"),
    path('add_address/', views.add_address, name= "add_address"),
    path('edit_address/<pk>', views.edit_address, name= "edit_address"),
    path('delete_address/<pk>', views.delete_address, name= "delete_address"),
    path('change_password/', views.change_password, name= "change_password"),
    path('wallet/', views.wallet, name= "wallet"),  
]
