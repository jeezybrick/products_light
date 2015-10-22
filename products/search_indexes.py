
from django.db.models import Avg
from haystack import indexes
from products.models import Item, Comment, Rate
from my_auth.models import MyUser
from products.utils import get_min_quantity


class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.CharField(model_attr='id')
    author = indexes.CharField(model_attr='user')
    name = indexes.CharField(model_attr='name')
    price = indexes.IntegerField(model_attr='price')
    description = indexes.CharField(model_attr='name')
    image_url = indexes.CharField(model_attr='image_url')
    categories = indexes.MultiValueField(faceted=True)
    shops = indexes.MultiValueField(faceted=True)
    comments = indexes.MultiValueField()
    rate = indexes.FloatField()
    quantity = indexes.IntegerField(model_attr='quantity', null=True)
    quantity_message = indexes.CharField()
    action = indexes.IntegerField()

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

    def prepare_quantity_message(self, obj):
        if obj.quantity is not None:
            if obj.quantity == 0:
                return 'The item is out of stock :('  # No i18n support
            if obj.quantity < get_min_quantity():
                return 'This item end soon! Hurry up!'
        return None

    def prepare_action(self, obj):
        try:
            obj.action.new_price
        except:
            return None

        return obj.action.new_price

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
