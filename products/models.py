from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(_("Имя"), max_length=50, blank=False)
    parent_category = models.ForeignKey("self", blank=True, null=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(_("Имя товара"), max_length=100, blank=False)
    price = models.IntegerField(_("Цена"), blank=False)
    image_url = models.URLField(_("Ссылка на изображние"), null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True, null=True)
    description = models.CharField(_("Описание"), max_length=1000, blank=False)

    def __str__(self):
        return self.name


class Comment(models.Model):
    username = models.CharField(_("Имя пользователя"), max_length=50, blank=False)
    message = models.CharField(_("Ваш комментарий"), max_length=1000, blank=False)
    item = models.ForeignKey(Item, related_name='comments')

    def __str__(self):
        return self.message


class Rate(models.Model):
    value = models.IntegerField()
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item, related_name='rates')

    def __str__(self):
        return self.value