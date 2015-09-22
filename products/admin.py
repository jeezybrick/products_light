from django.contrib import admin
from products import models

# Register your models here.

admin.site.register(models.Item)
admin.site.register(models.Category)
admin.site.register(models.Comment)