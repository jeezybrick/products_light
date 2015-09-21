__author__ = 'user'
from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from products.models import Item
from .serializers import ItemSerializer, UserSerializer
from rest_framework.response import Response
from haystack.query import SearchQuerySet
from django.http import QueryDict


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
    serializer_class = ItemSerializer


class ItemDetail(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer