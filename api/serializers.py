from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from products import models
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
        category = get_object_or_404(models.Category, id=obj.pk)
        return category.item_set.count()

    class Meta:
        model = models.Category
        fields = ('name', 'id', 'category_set', 'count', )


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        fields = ('username', 'message', 'item')

    def validate_message(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Text is too short!")
        return value


class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Rate
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
    in_cart = serializers.SerializerMethodField()

    def get_in_cart(self, obj):
        request = self.context.get('request', None)
        try:
            request.user.cart_set.get(item__id=obj.pk)
        except:
            in_cart = False
        else:
            in_cart = True

        return in_cart

    class Meta:

        fields = ('pk', 'name', 'price', 'description',
                  'categories', 'comments', 'image_url', 'rate', 'in_cart')


class ItemDetailSerializer(serializers.ModelSerializer):

    rates = serializers.SerializerMethodField(read_only=True)
    comments = CommentSerializer(many=True, required=False, read_only=True)
    categories = serializers.StringRelatedField(
        many=True, required=False, read_only=True)
    user_rate = serializers.SerializerMethodField()

    def get_rates(self, obj):
        return cache.RateCache().get(item_id=obj.pk).aggregate(Avg('value'))['value__avg']

    def get_user_rate(self, obj):
        request = self.context.get('request', None)
        try:
            user_rate = models.Rate.objects.get(
                user=request.user.id, item=obj.id).value
        except:
            user_rate = None

        return user_rate

    class Meta:
        model = models.Item
        fields = ('id', 'name', 'price', 'description', 'categories',
                  'comments', 'image_url', 'rates', 'user_rate', )


class ShopSerializer(serializers.Serializer):

    pk = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    items = serializers.StringRelatedField(many=True)

    class Meta:

        fields = ('pk', 'username', 'email', 'items', )


class ShopDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MyUser
        fields = ('id', 'username', 'email', 'items', )


class CartSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Cart
        fields = ('user', 'item', )