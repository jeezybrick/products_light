from django.db import models
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=50, blank=False)
    parent_category = models.ForeignKey("self", blank=True, null=True)

    def __str__(self):
        return self.name
