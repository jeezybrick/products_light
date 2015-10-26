from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404
from my_auth.models import MyUser
from cacheback.base import Job


class ShopDetailCache(Job):

    def fetch(self, **kwargs):
        if not self.model:
            raise ImproperlyConfigured(
                "%(cls)s is missing a model. Define %(cls)s.model %(cls)s.fetch()." % {
                    'cls': self.__class__.__name__
                }
            )

        obj = get_object_or_404(self.model, **kwargs)
        return obj

    model = MyUser
