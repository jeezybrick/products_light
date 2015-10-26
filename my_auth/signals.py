
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from my_auth.models import MyUser
from my_auth.cache import ShopDetailCache


invalidate_signals = [post_delete, post_save]


@receiver(post_save, sender=MyUser)
def invalidate_shop(sender, instance, **kwargs):
    ShopDetailCache().invalidate(id=str(instance.pk))
