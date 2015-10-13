from django.db import models
from products.models import Item
from django.conf import settings


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    item = models.ForeignKey(Item)

    def __unicode__(self):
        return self.user
