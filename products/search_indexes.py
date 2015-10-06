__author__ = 'user'
from django.db.models import Avg
from haystack import indexes
from products.models import Item, Comment, Rate, MyUser


class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    price = indexes.IntegerField(model_attr='price')
    description = indexes.CharField(model_attr='name')
    image_url = indexes.CharField(model_attr='image_url')
    categories = indexes.MultiValueField(faceted=True)
    shops = indexes.MultiValueField(faceted=True)
    comments = indexes.MultiValueField()
    rate = indexes.FloatField()
    # in_cart = indexes.BooleanField()

    def get_model(self):
        return Item

    def prepare_categories(self, obj):
        return [category.name for category in obj.categories.order_by('-id')]

    def prepare_comments(self, obj):
        return [comment.message for comment in obj.comments.order_by('-id')]

    def prepare_rate(self, obj):
        return obj.rates.aggregate(Avg('value'))['value__avg']

    def prepare_shops(self, obj):
        return obj.user.username
    """
    def prepare_in_cart(self, obj, request):
        try:
            self.request.user.cart_set.get(item__id=obj.pk)
        except:
            in_cart = False
        else:
            in_cart = True

        return in_cart
    """
    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class ShopIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    username = indexes.CharField(model_attr='username')
    email = indexes.CharField(model_attr='email')
    items = indexes.MultiValueField(faceted=True)
    is_shop = indexes.BooleanField(model_attr='is_shop')

    def get_model(self):
        return MyUser

    def prepare_items(self, obj):
        return [item.name for item in obj.items.order_by('-id')]

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
