from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from categories.models import Category
from core.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Item(TimeStampedModel):
    name = models.CharField(_("Name of item"), max_length=100, blank=False)
    price = models.IntegerField(_("Price"), blank=False)
    image_url = models.URLField(_("Link to image"), blank=True, max_length=50)
    categories = models.ManyToManyField(Category, blank=True)
    description = models.CharField(
        _("Description"), max_length=1000, blank=False)
    quantity = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items')

    def __str__(self):
        return self.name


class Comment(TimeStampedModel):
    username = models.CharField(_("Username"), max_length=50, blank=False)
    message = models.CharField(_("Comment"), max_length=1000, blank=False)
    item = models.ForeignKey(Item, related_name='comments')

    def __str__(self):
        return self.message


class Rate(models.Model):
    value = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    item = models.ForeignKey(Item, related_name='rates')

    def __unicode__(self):
        return self.value


class Action(models.Model):
    item = models.OneToOneField(Item)
    shop = models.ForeignKey(settings.AUTH_USER_MODEL)
    description = models.CharField(max_length=1000)
    new_price = models.IntegerField(blank=True)
    period_from = models.DateField()
    period_to = models.DateField()

    def __unicode__(self):
        return self.item
