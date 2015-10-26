from cart.models import Cart


class CartService:

    def get_cart(self, user, **kwargs):
        return Cart.objects.filter(user_id=user.id, **kwargs)
