__author__ = 'user'
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, viewsets, status
from rest_framework.pagination import PageNumberPagination
from products.models import Item, Category, Rate, Comment
from api import serializers
from rest_framework.response import Response
from haystack.query import SearchQuerySet
from django.http import QueryDict


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 2


class ItemList(generics.GenericAPIView):

    # pagination_class = StandardResultsSetPagination

    def get(self, request, format=None):
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

        serializer = serializers.ItemSerializer(queryset, many=True)
        headers = {'faceting': SearchQuerySet().models(Item).facet('categories').facet_counts()}
        return Response(serializer.data, headers=headers)


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