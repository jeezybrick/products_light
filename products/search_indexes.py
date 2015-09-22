__author__ = 'user'

from haystack import indexes
from products.models import Item, Comment, Rate, Category


class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.CharField(model_attr='id')
    name = indexes.CharField(model_attr='name')
    price = indexes.IntegerField(model_attr='price')
    description = indexes.CharField(model_attr='name')
    image_url = indexes.CharField(model_attr='image_url')
    categories = indexes.MultiValueField(faceted=True)
    comments = indexes.MultiValueField()

    def get_model(self):
        return Item

    def prepare_categories(self, obj):
        return [category.name for category in obj.categories.order_by('-id')]

    def prepare_comments(self, obj):
        return [comment.name for comment in obj.comment_set.order_by('-id')]

    def prepare_description(self, obj):

        description = None

        if 'description' in self.prepared_data:
            description = 'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT'
            
        return description

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