from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from .models import Item, Category
from .cache import ProductCache, CategoryCache


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff', )


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent_category', )


class ItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Item
        fields = ('id', 'url', 'name', 'price', 'description', 'image_url', 'categories', )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ItemViewSet(viewsets.GenericViewSet):
    queryset = ProductCache().get()
    serializer_class = ItemSerializer

    def list(self, request, *args, **kwargs):
        """
        List of available filters for cruise search
        lang -- language (en or zh-cn)
        """
        data_list = ProductCache().get()
        return HttpResponse(self.serializer_class(data_list).data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = CategoryCache().get()
    serializer_class = CategorySerializer