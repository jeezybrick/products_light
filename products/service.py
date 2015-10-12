from products import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from django.shortcuts import get_object_or_404


class CartService:

    def get_cart(self, user, **kwargs):
        return models.Cart.objects.filter(user_id=user.id, **kwargs)


class RateService:

    def get_rate(self, user, item_id):
        return models.Rate.objects.filter(user_id=user.id, item=item_id).first()

    def get_user_rate(self, user, item_id):
        try:
            user_rate = models.Rate.objects.get(user_id=user.id, item=item_id).value
        except ObjectDoesNotExist:
            user_rate = None
        return user_rate

    def get_avarage_rate(self, item_id):
        return models.Rate.objects.filter(item_id=item_id).aggregate(Avg('value'))
