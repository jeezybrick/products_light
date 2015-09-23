__author__ = 'user'
from statistics import mean
from django.db.models import Avg
from haystack import indexes
from products.models import Item, Comment, Rate, Category


class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # id = indexes.CharField(model_attr='id')
    name = indexes.CharField(model_attr='name')
    price = indexes.IntegerField(model_attr='price')
    description = indexes.CharField(model_attr='name')
    image_url = indexes.CharField(model_attr='image_url')
    categories = indexes.MultiValueField(faceted=True)
    rate = indexes.FloatField()

    def get_model(self):
        return Item

    def prepare_categories(self, obj):
        return [category.name for category in obj.categories.order_by('-id')]

    def prepare_rate(self, obj):
        return obj.rates.aggregate(Avg('value'))['value__avg']

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class CommentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    item = indexes.CharField(model_attr='item', faceted=True)

    def get_model(self):
        return Comment

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class RateIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    user = indexes.CharField(model_attr='user', faceted=True)
    item = indexes.CharField(model_attr='item', faceted=True)

    def get_model(self):
        return Rate

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

"""
dddddddddddddddddddddddddddddd
class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    items = indexes.MultiValueField(faceted=True)

    def get_model(self):
        return Category

    def prepare_items(self, obj):
        return [item.name for item in obj.items.order_by('-id')]

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
"""
