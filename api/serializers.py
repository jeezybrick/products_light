from rest_framework import routers, serializers, viewsets, generics
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from products.models import Item, Category, Rate, Comment
from haystack.query import SearchQuerySet
from django.db.models import Avg
from products import cache


class UserSerializer(serializers.ModelField):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff', )


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    category_set = serializers.StringRelatedField(many=True)
    count = serializers.SerializerMethodField()

    def get_count(self, obj):
        category = get_object_or_404(Category, id=obj.pk)
        return category.item_set.count()
    '''
    def get_count_sub(self, obj):
        category = get_object_or_404(Category, id=obj.pk)
        sub = category.category_set.all()
        return sub.item_set.count()
    '''
    class Meta:
        model = Category
        fields = ('name', 'id', 'category_set', 'count', )


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('username', 'message', 'item')


class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = ('value', 'item')


class ItemSerializer(serializers.Serializer):

    pk = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.IntegerField()
    description = serializers.CharField()
    image_url = serializers.URLField()
    categories = serializers.StringRelatedField(many=True)
    comments = serializers.StringRelatedField(many=True)
    rate = serializers.FloatField()

    class Meta:

        fields = ('pk', 'name', 'price', 'description', 'categories', 'comments', 'image_url', 'rate', )


class ItemDetailSerializer(serializers.ModelSerializer):

    rates = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True)
    categories = serializers.StringRelatedField(many=True)

    def get_rates(self, obj):
         return cache.RateCache().get(item_id=obj.pk).aggregate(Avg('value'))['value__avg']

    class Meta:
        model = Item
        fields = ('id', 'name', 'price', 'description', 'categories', 'comments', 'image_url', 'rates', )