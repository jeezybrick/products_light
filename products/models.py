from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=50, blank=False)
    parent_category = models.ForeignKey("self", blank=True, null=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(_("Name of item"), max_length=100, blank=False)
    price = models.IntegerField(_("Price"), blank=False)
    image_url = models.URLField(_("Link to image"), null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    description = models.CharField(
        _("Description"), max_length=1000, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    username = models.CharField(_("Username"), max_length=50, blank=False)
    message = models.CharField(_("Comment"), max_length=1000, blank=False)
    item = models.ForeignKey(Item, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.message


class Rate(models.Model):
    value = models.IntegerField()
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item, related_name='rates')

    def __unicode__(self):
        return self.value
