from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin, name= "signin"),
    path('signup/', views.signup, name= "signup"),
    path('signout/', views.signout, name= "signout"),
    path('otp_verification/<pk>/', views.otp_verification, name= "otp_verification"),
    path('profile/', views.profile, name= "profile"),
    path('edit_profile/', views.edit_profile, name= "edit_profile"),

    
]
