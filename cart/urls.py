from django.urls import path
from cart import views

urlpatterns = [
    path('', views.cart_summary, name='cart_summary'),
    path('finalcheck/', views.cart_finalcheck, name='cart_finalcheck'),
    path('add/', views.cart_add, name='cart_add'),
    path('delete/', views.cart_delete, name='cart_delete')
]