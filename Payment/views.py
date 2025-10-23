from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from cart.cart import Cart
from MainPage.models import DeliveryInfoProfile, Product
from .models import Order, OrderItem
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# Create your views here.

def create_order(request):
    if request.method == 'POST':
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantity = cart.get_quants()
        total = cart.get_total()

        user_id = request.POST.get("user_delivery_id")
        delivery_info = DeliveryInfoProfile.objects.get(user__id = user_id)
        user_account_info = User.objects.get(id = user_id)

        if request.user.is_authenticated:
            user = request.user
            new_order = Order(
                user = user ,
                full_name = delivery_info.full_name ,
                phone = delivery_info.phone ,
                email = user_account_info.email ,
                delivery_address = delivery_info.address ,
                amount_paid = total
            )
            new_order.save()

            order = get_object_or_404(Order, id = new_order.pk)
            for product in cart_products:
                prod = get_object_or_404(Product, id = product.id)
                
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                for k,v in quantity.items():
                    if int(k) == product.id:
                        new_item = OrderItem(
                            order = order ,
                            user = user ,
                            products = prod ,
                            quantity = v ,
                            price = price
                        )
                        new_item.save()
                
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]
            
            deliveryinfo = DeliveryInfoProfile.objects.filter(user__id = user_id)
            deliveryinfo.update(shopping_cart="")

            messages.success(request, ('سفارش شما با موفقیت ثبت شد!'))
            messages.success(request, ('از بخش | پیگیری سفارشات من | در پروفایل اقدام به پرداخت مبلغ نمایید'))
            return redirect('home')
        else:
            messages.success(request, ('ابتدا وارد حساب خود شوید!'))
            return redirect('home')
    else:
        messages.success(request, ('دسترسی به این صفحه امکان پذیر نمی باشد!'))
        return redirect('home')
    
def user_orders(request):
    if request.user.is_authenticated:
        active_orders = Order.objects.filter(user__id = request.user.id).exclude(status__in=['canceled','Delivered'])
        canceled_orders = Order.objects.filter(user__id = request.user.id, status='canceled')
        delivered_orders = Order.objects.filter(user__id = request.user.id, status='Delivered')
        
        orders_dict = {'active_orders':active_orders , 
                       'canceled_orders':canceled_orders, 
                       'delivered_orders':delivered_orders
                    }
        
        return render(request, 'user_orders.html', orders_dict)
    else:
        messages.success(request, ('ابتدا باید وارد حساب کاربری خود شوید!'))
        return redirect('home')
    
def user_order_details(request, pk):
    if request.user.is_authenticated:
        order = Order.objects.filter(id = pk)
        order_items = OrderItem.objects.filter(order__id = pk)
        return render(request, 'order_details.html', {'order':order , 'order_items':order_items})
    else:
        messages.success(request, ('دسترسی به این صفحه امکان پذیر نمی باشد!'))
        return redirect('home')

def cancel_order(request, order_id):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, id=order_id)
        order.status = 'canceled'
        order.save()
        messages.success(request, ('سفارش شما لغو گردید!'))
        return redirect('user_orders')
    else:
        messages.success(request, ('دسترسی به این صفحه مجاز نمی باشد!'))
        return redirect('home')


    

