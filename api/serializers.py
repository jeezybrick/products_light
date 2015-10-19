from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from products import models
from categories.models import Category
from cart.models import Cart
from cart.service import CartService
from my_auth.models import MyUser


class UserSerializer(serializers.ModelField):

    class Meta:
        model = MyUser
        fields = ('url', 'username', 'email', 'is_staff', )


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    category_set = serializers.StringRelatedField(many=True)
    count = serializers.SerializerMethodField()

    def get_count(self, obj):
        category = get_object_or_404(Category, id=obj.pk)
        return category.item_set.count()

    class Meta:
        model = Category
        fields = ('name', 'id', 'category_set', 'count', )


class CommentSerializer(serializers.ModelSerializer):

    max_message_length = 5

    class Meta:
        model = models.Comment
        fields = ('username', 'message', 'item')

    def is_message_not_valid(self, value):
        return len(value) < self.max_message_length

    def validate_message(self, message):
        if self.is_message_not_valid(message):
            raise serializers.ValidationError(_("Text is too short!"))
        return message


class RateSerializer(serializers.ModelSerializer):

    max_value = 10
    min_value = 0

    def is_value_not_valid(self, value):
        return value > self.max_value or value < self.min_value

    def validate_value(self, value):
        if self.is_value_not_valid(value):
            raise serializers.ValidationError(_("Invalid value!"))
        return value

    class Meta:
        model = models.Rate
        fields = ('value', 'item')


class ItemSerializer(serializers.Serializer):

    pk = serializers.IntegerField()
    author = serializers.CharField(read_only=True)
    name = serializers.CharField()
    price = serializers.IntegerField()
    description = serializers.CharField()
    image_url = serializers.URLField()
    categories = serializers.StringRelatedField(many=True)
    comments = serializers.StringRelatedField(many=True)
    rate = serializers.FloatField()
    quantity = serializers.IntegerField()
    quantity_message = serializers.CharField()
    is_item_in_cart = serializers.SerializerMethodField()
    action = serializers.IntegerField()

    def get_is_item_in_cart(self, obj):
        request = self.context.get('request', None)
        if request:
            return CartService().get_cart(request.user, item_id=obj.pk).exists()
        else:
            return False

    class Meta:

        fields = ('pk', 'author', 'name', 'price', 'description',
                  'categories', 'comments', 'image_url', 'rate', 'quantity',
                  'in_cart', 'quantity_message', 'action', )


class ItemDetailSerializer(serializers.ModelSerializer):

    rates = serializers.SerializerMethodField(read_only=True)
    comments = CommentSerializer(many=True, required=False, read_only=True)
    categories = serializers.StringRelatedField(
        many=True, required=False, read_only=True)
    user_rate = serializers.SerializerMethodField()
    action_price = serializers.SerializerMethodField()
    user = serializers.CharField(read_only=True)

    def get_rates(self, obj):
        return models.Rate.objects.average(item_id=obj.pk)

    def get_user_rate(self, obj):

        request = self.context.get('request', None)
        user_rate = models.Rate.objects.auth_user_rating(user_id=request.user.id, item_id=obj.pk)

        return user_rate

    """ get action price"""

    def get_action_price(self, obj):
        request = self.context.get('request', None)
        try:
            price = models.Action.objects.get(
                shop=request.user.id, item=obj.id).new_price
        except ObjectDoesNotExist:
            price = None

        return price

    class Meta:
        model = models.Item
        fields = ('id', 'user', 'name', 'price', 'description', 'categories',
                  'comments', 'image_url', 'rates', 'user_rate', 'quantity', 'action_price', )


class ShopSerializer(serializers.Serializer):

    pk = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    items = serializers.StringRelatedField(many=True)

    class Meta:

        fields = ('pk', 'username', 'email', 'items', )


class ShopDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email', 'items', )


class CartSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Cart
        fields = ('user', 'item', )


class ActionSerializer(serializers.ModelSerializer):

    max_price = 1000000
    min_price = 0

    def is_price_not_valid(self, value):
        return value > self.max_price or value < self.min_price

    def validate_new_price(self, price):
        if self.is_price_not_valid(price):
            raise serializers.ValidationError(_("Invalid price!"))
        return price

    class Meta:
        model = models.Action
        fields = ('item', 'description', 'new_price',
                  'period_from', 'period_to', )
