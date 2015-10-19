from django.db import models
from django.db.models import Avg
from django.core.exceptions import ObjectDoesNotExist


class RateManager(models.Manager):
    use_for_related_fields = True

    def average(self, **kwargs):
        return self.filter(**kwargs).aggregate(Avg('value'))['value__avg']

    def auth_user_rating(self, ** kwargs):
        try:
            user_rate = super(RateManager, self).get_queryset().get(**kwargs).value
        except ObjectDoesNotExist:
            user_rate = None
        return user_rate
