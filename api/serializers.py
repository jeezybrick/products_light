from rest_framework import routers, serializers, viewsets, generics
from django.contrib.auth.models import User
from products.models import Item, Category, Rate
from django.db.models import Avg
from products.cache import ProductCache, CategoryCache


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff', )


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    category_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = Category
        fields = ('name', 'id', 'category_set')


class ItemSerializer(serializers.HyperlinkedModelSerializer):

    categories = serializers.StringRelatedField(many=True)
    fav = serializers.SerializerMethodField('get_rate')

    def get_rate(self, obj):
        return Rate.objects.filter(item_id=obj.id).aggregate(Avg('value'))

    class Meta:
        model = Item
        fields = ('id', 'url', 'name', 'price', 'description', 'image_url', 'categories', 'fav', )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(parent_category_id__isnull=True)
    serializer_class = CategorySerializer


