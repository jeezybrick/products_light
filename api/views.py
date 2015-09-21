__author__ = 'user'
from rest_framework import generics
from products.models import Item
from .serializers import ItemSerializer


class ItemList(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer