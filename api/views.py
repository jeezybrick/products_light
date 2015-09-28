__author__ = 'user'
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import Http404
from django.db import models
from rest_framework import generics, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from products.models import Item, Category, Rate, Comment
from products import cache
from api import serializers
from rest_framework.response import Response
from haystack.query import SearchQuerySet
from haystack import signals


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1


class ItemList(generics.GenericAPIView):

    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.ItemSerializer

    def get(self, request, format=None):
        try:
            request.GET["category"]
        except:
            queryset = SearchQuerySet().models(cache.ProductCache.model).order_by('-id')
        else:
            queryset = SearchQuerySet().models(cache.ProductCache.model).filter(categories__in=[request.GET["category"]])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.ItemSerializer(queryset, many=True)
        return Response(serializer.data)


class ItemDetail(generics.RetrieveAPIView):

    queryset = Item.objects.all()
    serializer_class = serializers.ItemDetailSerializer

    def get_object(self):

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = cache.ProductDetailCache().get(id=filter_kwargs['pk'])
        self.check_object_permissions(self.request, obj)

        return obj


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class CategoryList(APIView):

    def get(self, request, format=None):
        categories = cache.CategoryCache().get(parent_category_id__isnull=True)
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CommentList(APIView):

    def get(self, request, format=None):
        comments = cache.CommentCache().get()
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data)


class RateList(APIView):

    def get(self, request, format=None):
        rates = cache.RateCache().get()
        serializer = serializers.RateSerializer(rates, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            rate = Rate.objects.get(user=request.user.id, item=request.data["item"])
        except:
            rate = None
        serializer = serializers.RateSerializer(data=request.data, instance=rate)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)