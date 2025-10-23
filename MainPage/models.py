from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator , MaxValueValidator

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'Category - {self.name}'
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    picture = models.ImageField(upload_to='upload/products/')
    price = models.DecimalField(default=0, decimal_places=0, max_digits=12)

    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=0, max_digits=12)

    def __str__(self):
        return f'Product - {self.name}'

class StaffRole(models.Model):
    ROLES = [
        ('Manager','مدیر'),
        ('Waiter','گارسون'),
        ('Chef','سرآشپز'),
        ("Chef's Assistant","کمک آشپز"),
        ('Cashier','صندوق دار'),
        ('Delivery Guy','پیک')
    ]
    name = models.CharField(choices=ROLES, default='Waiter')

    def __str__(self):
        return f'Role - {self.name}' 

class Staff(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.ForeignKey(StaffRole, on_delete=models.CASCADE)
    birth = models.IntegerField(default=1960, validators=[MinValueValidator(1960), MaxValueValidator(2025)])
    country = models.CharField(max_length=50, default='IRAN')
    picture = models.ImageField(upload_to='upload/staff/')
    bio = models.TextField(max_length=150000, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null =True)
    email = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return f'Staff | {self.first_name} {self.last_name} : {self.role}'
    
class DeliveryInfoProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=25, blank=True)
    address = models.TextField(max_length=400, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    shopping_cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'Delivery Info - {self.user.username}'

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = DeliveryInfoProfile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)
