__author__ = 'user'

from .models import Category


def categories_as_choices():
    return [[category.id, category.name] for category in Category.objects.filter(parent_category_id__isnull=True)]
