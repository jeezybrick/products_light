from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from core.models import TimeStampedModel
from my_auth.managers import CustomUserManager


# Extend User model
class MyUser(AbstractUser, TimeStampedModel):

    is_shop = models.NullBooleanField(_("Shop"), default=True)
    percentage_of_price = models.IntegerField(default=100, null=True)

    USERNAME_FIELD = 'username'

    def __unicode__(self):
        return self.username

    class Meta(object):
        unique_together = ('email', )


class OAuthUser(AbstractBaseUser):

    username = models.CharField(max_length=30)
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return self.username

    def is_authenticated(self):
        return True
