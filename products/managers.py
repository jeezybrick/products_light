from django.db import models
from django.db.models import Avg


class AverageManager(models.Manager):
    use_for_related_fields = True

    def average(self, **kwargs):
        return self.filter(**kwargs).aggregate(Avg('value'))['value__avg']
