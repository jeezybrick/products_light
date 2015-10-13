from django.contrib import admin
from products import models
from cart.models import Cart
from categories.models import Category

# Register your models here.

admin.site.register(models.MyUser)
admin.site.register(models.Item)
admin.site.register(Category)
admin.site.register(models.Comment)
admin.site.register(models.Rate)
admin.site.register(Cart)
admin.site.register(models.Action)