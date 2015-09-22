__author__ = 'user'
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from products.models import Item, Category, Rate, Comment
from api import serializers
from rest_framework.response import Response
from haystack.query import SearchQuerySet
from django.http import QueryDict


class ItemListTest(generics.GenericAPIView):

    serializer_class = serializers.ItemSerializer

    def list(self, request, *args, **kwargs):
        try:
            request.GET["category"]
        except:
            queryset = SearchQuerySet().models(Item).all()
        else:
            queryset = SearchQuerySet().models(Item).filter(categories__in=[request.GET["category"]])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ItemList(generics.ListAPIView):

    def list(self, request, *args, **kwargs):
        try:
            request.GET["category"]
        except:
            queryset = SearchQuerySet().models(Item).all()
        else:
            queryset = SearchQuerySet().models(Item).filter(categories__name=request.GET["category"])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # queryset = Item.objects.all()
    serializer_class = serializers.ItemSerializer


class ItemDetail(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = serializers.ItemSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(parent_category_id__isnull=True)
    serializer_class = serializers.CategorySerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = serializers.RateSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = serializers.ItemSerializer