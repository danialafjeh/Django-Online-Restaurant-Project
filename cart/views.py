from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .cart import Cart
from MainPage.models import Product, DeliveryInfoProfile

# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    total_price = cart.get_total()
    return render(request, 'cart_summary.html', {'products':cart_products, 'quantities':quantities, 'total_price':total_price})

def cart_finalcheck(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    total_price = cart.get_total()
    user_delivery_info = DeliveryInfoProfile.objects.get(user__id=request.user.id)
    info_dict = {
        'products':cart_products,
        'quantities':quantities, 
        'total_price':total_price, 
        'user_delivery':user_delivery_info
    }
    return render(request, 'cart_finalcheck.html', info_dict)
    
def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty)
        cart_quantity = cart.__len__()
        
        #response = JsonResponse({'product name':product.name})
        response = JsonResponse({'qty':cart_quantity})
        messages.success(request, ("به سبد خرید شما اضافه شد!"))
        return response

def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        response = JsonResponse({'product':product_id})
        messages.success(request, ("از سبد خرید شما حذف شد!"))
        return response