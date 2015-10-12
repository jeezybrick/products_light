from products import models


class CartService:

    def get_cart(self, user, **kwargs):
        return models.Cart.objects.filter(user_id=user.id, **kwargs)
