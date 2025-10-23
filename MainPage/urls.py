from django.urls import path, include
from MainPage import views

urlpatterns = [
    path('', views.home, name='home'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('contactus/', views.contactus, name='contactus'),
    path('product/<str:cat>', views.product, name='product'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_user, name='signup'),
    path('profile_user/', views.profile_user, name='profile_user'),
    path('update_profile_user/', views.update_profile, name='update_profile'),
    path('update_password/', views.update_password, name='update_password'),
    path('deliveryinfo/', views.deliveryinfo_profile, name='deliveryinfo')
]