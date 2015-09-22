from rest_framework import routers, serializers, viewsets, generics
from django.contrib.auth.models import User
from products.models import Item, Category, Rate, Comment
from django.db.models import Avg
from products.cache import ProductCache, CategoryCache


class UserSerializer(serializers.ModelField):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff', )


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    category_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = Category
        fields = ('name', 'id', 'category_set')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('username', 'message', 'item')


class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = ('value', 'user', 'item')


class ItemSerializer(serializers.Serializer):

    pk = serializers.CharField()
    name = serializers.CharField()
    price = serializers.IntegerField()
    description = serializers.CharField()
    image_url = serializers.CharField()
    categories = serializers.StringRelatedField(many=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:

        fields = ('pk', 'name', 'price', 'description', 'categories', 'comments', 'image_url', )
