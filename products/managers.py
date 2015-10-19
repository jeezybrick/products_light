from django.db import models
from django.db.models import Avg


class AverageRateManager(models.Manager):
    use_for_related_fields = True

    def average(self, **kwargs):
        return super(AverageRateManager, self).get_queryset().filter(**kwargs).aggregate(Avg('value'))['value__avg']

