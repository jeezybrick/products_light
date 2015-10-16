from django.contrib import admin
from products import models

# Register your models here.


class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "created_at", 'updated')


class CommentAdmin(admin.ModelAdmin):
    list_display = ("username", "message", "created_at", 'updated')


class RateAdmin(admin.ModelAdmin):
    list_display = ("user", "item", "value")


class ActionAdmin(admin.ModelAdmin):
    list_display = ("item", "shop", "new_price", "period_from", "period_to")

admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Rate, RateAdmin)
admin.site.register(models.Action, ActionAdmin)
