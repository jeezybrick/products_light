from rest_framework import routers, serializers, viewsets, generics
from django.contrib.auth.models import User
from products.models import Item, Category, Rate, Comment
from django.db.models import Avg
from products.cache import ProductCache, CategoryCache
from haystack.query import SearchQuerySet


class UserSerializer(serializers.HyperlinkedModelSerializer):
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


class ItemSerializer(serializers.ModelSerializer):

    categories = serializers.StringRelatedField(many=True)
    fav = serializers.SerializerMethodField('get_rate')
    comments = CommentSerializer(many=True, read_only=True)

    def get_rate(self, obj):
        return Rate.objects.filter(item_id=obj.id).aggregate(Avg('value'))

    class Meta:
        model = Item
        fields = ('id', 'url', 'name', 'price', 'description', 'image_url', 'categories', 'fav', 'comments', )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(parent_category_id__isnull=True)
    serializer_class = CategorySerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
