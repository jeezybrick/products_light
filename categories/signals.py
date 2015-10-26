
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from categories.models import Category
from categories.cache import CategoryCache


invalidate_signals = [post_delete, post_save]


@receiver(invalidate_signals, sender=Category)
def invalidate_category(sender, instance, **kwargs):
    CategoryCache().invalidate(parent_category_id__isnull=True)
