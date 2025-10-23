from django.shortcuts import render, redirect
from MainPage.models import Staff, Category, Product, DeliveryInfoProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import json
from cart.cart import Cart
from MainPage.forms import SignUpForm , UpdateUserForm, UpdatePasswordForm, DeliveryInfoForm

# Create your views here.

def home(request):
    all_cat = Category.objects.all()
    all_prods = Product.objects.all()
    return render(request, 'home.html',{'category':all_cat, 'products':all_prods})

def aboutus(request):
    staff = Staff.objects.all()
    return render(request, 'about.html', {'staff':staff})

def contactus(request):
    return render(request, 'contact.html', {})

def product(request, cat):
    cat = cat.replace("-"," ")
    category = Category.objects.get(name=cat)
    products = Product.objects.filter(category=category)
    return render(request, 'product.html', {'category':category, 'products':products})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            current_user = DeliveryInfoProfile.objects.get(user__id = request.user.id)
            saved_cart = current_user.shopping_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)

                for k,v in converted_cart.items():
                    cart.db_add(product=k , quantity=v)

            messages.success(request,('با موفقیت وارد اکانت خود شدید!'))
            return redirect('home')
        else:
            messages.success(request, ('مشکلی در ورود به اکانت شما وجود داشت!'))
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, ('با موفقیت از اکانت خود خارج شدید!'))
    return redirect('home')

def signup_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password1)
            login(request, user)
            messages.success(request,("حساب شما با موفقیت ساخته شد!"))
            return redirect('deliveryinfo')
        else:
            messages.success(request,("مشکلی در ثبت نام شما وجود داشت!"))
            return redirect('signup')
    else:
        return render(request, 'signup.html',{'form':form})
    
def deliveryinfo_profile(request):
    if request.user.is_authenticated:
        current_user = DeliveryInfoProfile.objects.get(user__id=request.user.id)
        form_delivery = DeliveryInfoForm(instance=current_user)
        if request.method == 'POST':
            form_delivery = DeliveryInfoForm(request.POST, instance=current_user)
            if form_delivery.is_valid():
                form_delivery.save()
                messages.success(request, ('مشخصات ارسال سفارش برای حساب شما ثبت شد!'))
                return redirect('home')
            else:
                messages.success(request,("مشکلی در ثبت طالاعات وجود داشت!"))
                return redirect('deliveryinfo')
        else:
            return render(request, 'deliveryinfo_profile.html', {'form_delivery':form_delivery})
    else:
        messages.success(request,('ابتدا باید وارد حساب کاربری خود شوید!'))
        return redirect('home')
                
def profile_user(request):
    user_account_info = User.objects.get(id=request.user.id)
    user_delivery_info = DeliveryInfoProfile.objects.get(user__id=request.user.id)
    return render(request, 'profile_user.html', 
                  {'user_account':user_account_info , 'user_delivery':user_delivery_info})

def update_profile(request):
    if request.user.is_authenticated:
       current_user = User.objects.get(id=request.user.id)
       form = UpdateUserForm(instance = current_user)
       if request.method == 'POST':
           form = UpdateUserForm(request.POST, instance = current_user)
           if form.is_valid():
               form.save()
               login(request, current_user)
               messages.success(request, ('اطلاعات حساب شما ویرایش شد!'))
               return redirect('profile_user')
           else:
               messages.success(request,("مشکلی در ویرایش اطلاعات وجود داشت!"))
               return redirect('update_profile')
       else:
           return render(request, 'update_profile.html', {'form':form})
    else:
        messages.success(request,('ابتدا باید وارد حساب کاربری خود شوید!'))
        return redirect('home')
       
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        form_pass = UpdatePasswordForm(current_user)
        if request.method =='POST':
            form_pass = UpdatePasswordForm(current_user, request.POST)
            if form_pass.is_valid():
                form_pass.save()
                messages.success(request,('رمز شما با موفقیت ویرایش شد!'))
                login(request, current_user)
                return redirect('profile_user')
            else:
                for error in list(form_pass.errors.values()):
                    messages.error(request,(error))
                return redirect('update_password')
        else:
            return render(request,'update_password.html',{'form_pass':form_pass})
    else:
        messages.success(request,('ابتدا باید وارد حساب کاربری خود شوید!'))
        return redirect('home')
