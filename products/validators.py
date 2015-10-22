from django.core.exceptions import PermissionDenied


# Return PermissionDenied if auth user is not a shop
def if_user_not_a_shop(self):
        if not self.request.user.is_shop:
            raise PermissionDenied
