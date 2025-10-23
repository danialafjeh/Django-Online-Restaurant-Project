from django.contrib.auth.models import User
from MainPage.models import DeliveryInfoProfile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'type':'text', 'class':'form-control','placeholder':'نام'})
    )
    last_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'type':'text', 'class':'form-control','placeholder':' نام خانوادگی '})
    )
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'type':'email', 'class':'form-control','placeholder':'ایمیل'})
    )
    username = forms.CharField(
        label="",
        max_length=20,
        widget=forms.TextInput(attrs={'type':'text', 'class':'form-control', 'placeholder':'نام کاربری'})
    )
    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'name':'password',
            'type':'password',
            'placeholder': "رمز بالای 8 کاراکتر خود را وارد نمایید"
        }
        )
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'name':'password',
            'type':'password',
            'placeholder':'رمز خود را دوباره وارد کنید'
        }
        )
    )

    class Meta:
        model = User
        fields = ('first_name','last_name','email','username','password1','password2')


class UpdateUserForm(UserChangeForm):
    password = None

    first_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'type':'text', 'class':'form-control','placeholder':'نام'})
    )
    last_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'type':'text', 'class':'form-control','placeholder':' نام خانوادگی '})
    )
    username = forms.CharField(
        label="",
        max_length=20,
        widget=forms.TextInput(attrs={'type':'text', 'class':'form-control', 'placeholder':'نام کاربری'})
    )
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'type':'email', 'class':'form-control','placeholder':'ایمیل'})
    )

    class Meta:
        model = User
        fields = ('first_name','last_name','email','username')

class UpdatePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'رمز بالای 8 کاراکتر خود را وارد کنید',
            }
        )
    )
    new_password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'رمز خود را دوباره وارد کنید',
            }
        )
    )

    class Meta:
        model = User
        fields = ('new_password1','new_password2')


class DeliveryInfoForm(forms.ModelForm):
    full_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام کامل'}),
        required=True

    )
    phone = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شماره تماس'}),
        required=True

    )
    address = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'آدرس'}),
        required=True

    )
    city = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شهر'}),
        required=False

    )
    state = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'منطقه'}),
        required=False

    )

    class Meta:
        model = DeliveryInfoProfile
        fields = (
            'full_name',
            'phone',
            'address',
            'city',
            'state'
        ) 

   
    