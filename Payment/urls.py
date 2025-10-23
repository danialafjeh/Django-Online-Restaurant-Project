from django.urls import path
from . import views

urlpatterns = [
    path('create_order/', views.create_order, name='create_order'),
    path('user_orders/', views.user_orders, name='user_orders'),
    path('user_order_details/<int:pk>', views.user_order_details, name='order_details'),
    path('cancel_order/<int:order_id>', views.cancel_order, name='cancel_order')
]