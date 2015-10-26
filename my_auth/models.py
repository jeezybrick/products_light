from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from core.models import TimeStampedModel


# Extend User model
class MyUser(AbstractUser, TimeStampedModel):

    is_shop = models.NullBooleanField(_("Shop"), default=True)
    percentage_of_price = models.IntegerField(default=100, null=True)

    USERNAME_FIELD = 'username'

    def __unicode__(self):
        return self.username

    class Meta(object):
        unique_together = ('email', )
