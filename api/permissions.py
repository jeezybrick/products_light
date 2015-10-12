from rest_framework import permissions
from api.utils import is_safe_method
from products.models import Item, MyUser


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return True if is_safe_method(request) else obj.user == request.user


class ShopIsAuthorOrReadOnly(permissions.BasePermission):

    message = 'Only owner can add action'

    def has_permission(self, request, view):
        item = Item.objects.get(id=request.data['item'])
        return True if is_safe_method(request) else item.user == request.user
