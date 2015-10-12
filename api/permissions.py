from rest_framework import permissions
from api.utils import is_safe_method
from products.models import Item

""" check if auth user is author to this item """


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return True if is_safe_method(request) else obj.user == request.user


class ShopIsAuthorOrReadOnly(permissions.BasePermission):

    message = 'Only owner can add or edit action to this item'

    def has_permission(self, request, view):
        item_id = request.data.get('item', False)
        return True if is_safe_method(request) else Item.objects.filter(id=item_id, user_id=request.user.id).exists()
