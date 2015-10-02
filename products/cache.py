__author__ = 'user'
from django.core.exceptions import ImproperlyConfigured
from products.models import Item, Category, Rate, Comment
from cacheback.base import Job


class BaseModelJob(Job):
    model = None

    def key(self, *args, **kwargs):
        """Compose the key"""
        return "%s-%s" % (
            self.model.__name__,
            super(BaseModelJob, self).key(*args, **kwargs)
        )

    def fetch(self, **kwargs):
        if not self.model:
            raise ImproperlyConfigured(
                "%(cls)s is missing a model. Define %(cls)s.model %(cls)s.fetch()." % {
                    'cls': self.__class__.__name__
                }
            )

        obj = self.model.objects.filter(**kwargs)
        return obj


class ProductCache(BaseModelJob):
    model = Item


class ProductDetailCache(BaseModelJob):

    lifetime = 1

    def fetch(self, **kwargs):
        if not self.model:
            raise ImproperlyConfigured(
                "%(cls)s is missing a model. Define %(cls)s.model %(cls)s.fetch()." % {
                    'cls': self.__class__.__name__
                }
            )

        obj = self.model.objects.get(**kwargs)
        return obj

    model = Item


class CategoryCache(BaseModelJob):
    model = Category


class CommentCache(BaseModelJob):
    model = Comment


class RateCache(BaseModelJob):
    model = Rate
