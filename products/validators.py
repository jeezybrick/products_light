from django.core.exceptions import PermissionDenied


def if_user_not_a_shop(self):
        if not self.request.user.is_shop:
            raise PermissionDenied
