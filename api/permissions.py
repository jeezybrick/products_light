from django.utils.translation import ugettext_lazy as _
from rest_framework import permissions
from api.utils import is_safe_method
from products.models import Item, Action
from products.utils import get_min_quantity

""" check if auth user is author to this item """


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return True if is_safe_method(request) else obj.user == request.user


""" check if auth user is author to this item  and this user is shop"""


class ShopIsAuthorOrReadOnly(permissions.BasePermission):
    message = _('Only owner can add or edit action to this item')

    def has_permission(self, request, view):
        item_id = request.data.get('item', False)
        return True if is_safe_method(request) else Item.objects.filter(id=item_id, user_id=request.user.id).exists()


""" check if auth user is author of action"""


class IsAuthorOfActionOrReadOnly(permissions.BasePermission):
    message = _('Only owner can add or edit action to this item')

    def has_object_permission(self, request, view, obj):
        return True if is_safe_method(request) else Action.objects.filter(item_id=obj.item_id, shop_id=request.user.id).exists()

""" check if quantity of item = 0"""


class IsItemOutOfStock(permissions.BasePermission):
    message = _('Sorry,but this item out of stock')

    def has_permission(self, request, view):
        item_id = request.data.get('item', False)
        return True if is_safe_method(request) else not Item.objects.filter(id=item_id, quantity__exact=0).exists()
