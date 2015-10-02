__author__ = 'user'
from django.http import Http404
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from products.models import Item, Rate
from products import cache
from api import serializers
from rest_framework.response import Response
from haystack.query import SearchQuerySet


# Pagination class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 1


# Item list
class ItemList(generics.GenericAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.ItemSerializer

    def get(self, request):
        try:
            request.GET["category"]
        except:
            queryset = SearchQuerySet().models(Item).order_by('-id')
        else:
            queryset = SearchQuerySet().models(Item).filter(
                categories__in=[request.GET["category"]])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.ItemSerializer(queryset, many=True)
        return Response(serializer.data)


# Item detail
class ItemDetail(generics.RetrieveAPIView, generics.UpdateAPIView,
                 generics.DestroyAPIView):
    serializer_class = serializers.ItemDetailSerializer

    def get_object(self):

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            obj = cache.ProductDetailCache().get(id=filter_kwargs['pk'])
        except:
            raise Http404
        self.check_object_permissions(self.request, obj)

        return obj


# list of categories
class CategoryList(APIView):
    def get(self, request):
        categories = cache.CategoryCache().get(parent_category_id__isnull=True)
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data)


# Comments list
class CommentList(APIView):
    def get(self, request):
        comments = cache.CommentCache().get()
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Rating list
class RateList(APIView):
    def get(self, request):
        rates = cache.RateCache().get()
        serializer = serializers.RateSerializer(rates, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            rate = Rate.objects.get(
                user=request.user.id, item=request.data["item"])
        except:
            rate = None
        serializer = serializers.RateSerializer(
            data=request.data, instance=rate)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
