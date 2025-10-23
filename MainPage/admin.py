from django.contrib import admin
from django.contrib.auth.models import User
from MainPage import models

# Register your models here.

admin.site.register(models.StaffRole)
admin.site.register(models.Staff)
admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.DeliveryInfoProfile)

class ProfileInLine(admin.StackedInline):
    model = models.DeliveryInfoProfile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
        'is_superuser',
        'last_login',
        'date_joined'
        ]
    inlines = [ProfileInLine]
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


    