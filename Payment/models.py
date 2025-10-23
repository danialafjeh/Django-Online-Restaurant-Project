from django.db import models
from django.contrib.auth.models import User
from MainPage.models import Product
from django_jalali.db import models as jmodels
import jdatetime

# Create your models here.

class Order(models.Model):
    STATUS = [
        ('Pending','در انتظار پرداخت'),
        ('Processing','در حال آماده سازی سفارش'),
        ('On The Way','تحویل پیک موتوری داده شد'),
        ('Delivered','تحویل مشتری داده شد'),
        ('canceled','سفارش لغو شده است')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=25)
    email = models.EmailField(max_length=100)
    delivery_address = models.TextField(max_length=400)
    amount_paid = models.DecimalField(decimal_places=0, max_digits=20)
    date_ordered = jmodels.jDateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS, default='Pending')
    last_update = jmodels.jDateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old_status = Order.objects.get(id=self.pk).status
            if old_status != self.status:
                self.last_update = jdatetime.datetime.now()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order #{self.id} for {self.user.username}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    products = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(decimal_places=0, max_digits=12)

    def __str__(self):
        return f'Order Item #{self.id} in {self.order}'


