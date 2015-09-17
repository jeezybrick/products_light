__author__ = 'user'

from haystack import indexes
from products.models import Item


class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    price = indexes.IntegerField(model_attr='price')

    def get_model(self):
        return Item

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()