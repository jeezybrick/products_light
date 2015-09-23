__author__ = 'user'
from .models import Category, Item
from .cache import ProductCache, CategoryCache, RateCache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
invalidate_signals = [post_delete, post_save]


@receiver(invalidate_signals, sender=Category)
def invalidate_category(sender, instance, **kwargs):
    CategoryCache().invalidate()


@receiver(invalidate_signals, sender=Item)
def invalidate_item(sender, instance, **kwargs):
    ProductCache().invalidate(pk=instance.pk)


@receiver(post_save, sender=Item)
def invalidate_category(sender, instance, **kwargs):
    RateCache().invalidate()