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
    page_size = 9
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


class ItemDetail(APIView):

    def get_object(self, pk):
        try:
            return cache.ProductCache().get(id=pk)

        except cache.ProductCache().get(id=pk).DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = serializers.ItemDetailSerializer(item, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(parent_category_id__isnull=True)
    # queryset = cache.CategoryCache().get(parent_category_id__isnull=True)
    serializer_class = serializers.CategorySerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    # queryset = cache.CommentCache().get()
    serializer_class = serializers.CommentSerializer


class RateList(APIView, signals.BaseSignalProcessor):

    def get(self, request, format=None):
        rates = cache.RateCache().get()
        serializer = serializers.RateSerializer(rates, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.RateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)