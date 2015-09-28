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

    def validate_message(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Text is too short!")
        return value


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
    user_rate = serializers.SerializerMethodField()

    def get_rates(self, obj):
        return cache.RateCache().get(item_id=obj.pk).aggregate(Avg('value'))['value__avg']

    def get_user_rate(self, obj):
        request = self.context.get('request', None)
        try:
            user_rate = Rate.objects.get(user=request.user.id, item=obj.id).value
            # user_rate = cache.RateCache().get(user=request.user.id, item=obj.id)
        except:
            user_rate = None
        # return [user_rate.value for user_rate in user_rate]
        return user_rate

    class Meta:
        model = Item
        fields = ('id', 'name', 'price', 'description', 'categories', 'comments', 'image_url', 'rates', 'user_rate' )