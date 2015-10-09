
from django.http import Http404
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework import generics, status, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from products.models import Item, Rate, MyUser
from products import cache
from api import serializers
from rest_framework.response import Response
from haystack.query import SearchQuerySet
from api.permissions import IsAuthorOrReadOnly, ShopIsAuthorOrReadOnly


# Pagination class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 1


# Item list
class ItemList(generics.GenericAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.ItemSerializer

    def get(self, request):

        try:
            request.GET["category"]
        except MultiValueDictKeyError:
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
    permission_classes = (IsAuthorOrReadOnly, )

    def get_object(self):

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            obj = cache.ProductDetailCache().get(id=filter_kwargs['pk'])
        except ObjectDoesNotExist:
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
        if request.user.is_authenticated():
            try:
                rate = Rate.objects.get(
                    user=request.user.id, item=request.data["item"])
            except ObjectDoesNotExist:
                rate = None
            serializer = serializers.RateSerializer(
                data=request.data, instance=rate)
            if serializer.is_valid():
                serializer.save(user=self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise PermissionDenied

"""List of shop-users"""


class ShopList(generics.GenericAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.ShopSerializer

    def get(self, request):

        queryset = SearchQuerySet().models(MyUser).order_by('-id')
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.ShopSerializer(queryset, many=True)
        return Response(serializer.data)


# Detail of shop-users
class ShopDetail(generics.RetrieveAPIView):
    serializer_class = serializers.ShopDetailSerializer

    def get_object(self):

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            obj = cache.ShopCache().get(id=filter_kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404
        self.check_object_permissions(self.request, obj)

        return obj


""" List of items in cart for auth user """


class CartList(generics.GenericAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.CartSerializer
    permission_classes = (ShopIsAuthorOrReadOnly, permissions.IsAuthenticated)

    def get(self, request):

        queryset = self.request.user.cart_set.all()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.CartSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            item = self.request.user.cart_set.get(
                item__id=request.data["item"])
        except ObjectDoesNotExist:
            item = None
        serializer = serializers.CartSerializer(
            data=request.data, instance=item)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Detail of cart. ID is item_id
class CartDetail(generics.RetrieveAPIView, generics.UpdateAPIView,
                 generics.DestroyAPIView):

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.CartSerializer

    def get_object(self):

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            obj = self.request.user.cart_set.get(item__id=filter_kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404
        self.check_object_permissions(self.request, obj)

        return obj


# Action list and details for current auth user
class ActionList(generics.GenericAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.ActionSerializer
    permission_classes = (ShopIsAuthorOrReadOnly, permissions.IsAuthenticated)

    def get(self, request):

        queryset = self.request.user.action_set.all()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.ActionSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            action = self.request.user.action_set.get(
                item__id=request.data["item"])
        except (ObjectDoesNotExist, AttributeError):
            action = None
        serializer = serializers.ActionSerializer(
            data=request.data, instance=action)
        if serializer.is_valid():
            serializer.save(shop=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
