__author__ = 'user'
from .models import Category, Item, Rate,Comment
from .cache import ProductCache, CategoryCache, RateCache, CommentCache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.db import models
from haystack import signals

invalidate_signals = [post_delete, post_save]


@receiver(invalidate_signals, sender=Category)
def invalidate_category(sender, instance, **kwargs):
    CategoryCache().invalidate(parent_category_id__isnull=True)


@receiver(invalidate_signals, sender=Item)
def invalidate_item(sender, instance, **kwargs):
    ProductCache().invalidate(pk=instance.pk)


@receiver(post_save, sender=Rate)
def invalidate_rate(sender, instance, **kwargs):
    RateCache().invalidate()


@receiver(post_save, sender=Comment)
def invalidate_comment(sender, instance, **kwargs):
    CommentCache().invalidate()


class RateOnlySignalProcessor(signals.RealtimeSignalProcessor):

    def handle_rate_update(self, sender, instance, **kwargs):
        for item in Item.objects.filter(rates__id=instance.id):
            super(RateOnlySignalProcessor, self).handle_save(
                Item, item, **kwargs
            )

    def handle_comment_update(self, sender, instance, **kwargs):
        for comment in Item.objects.filter(comments__id=instance.id):
            super(RateOnlySignalProcessor, self).handle_save(
                Item, comment, **kwargs
            )

    def handle_category_update(self, sender, instance, **kwargs):
        for item in Item.objects.filter(id=instance.id):
            for category in item.categories.all():
                super(RateOnlySignalProcessor, self).handle_save(
                    Item, category, **kwargs
                )

    def setup(self, **kwargs):
        models.signals.post_save.connect(self.handle_save, sender=Item)
        models.signals.post_save.connect(self.handle_category_update, sender=Item)
        models.signals.post_delete.connect(self.handle_delete, sender=Item)
        models.signals.post_save.connect(self.handle_rate_update, sender=Rate)
        models.signals.post_delete.connect(self.handle_rate_update, sender=Rate)
        models.signals.post_save.connect(self.handle_comment_update, sender=Comment)
        models.signals.post_delete.connect(self.handle_comment_update, sender=Comment)

        super(RateOnlySignalProcessor, self).setup()

    def teardown(self):
        models.signals.post_save.disconnect(self.handle_save, sender=Item)
        models.signals.post_delete.disconnect(self.handle_delete, sender=Item)
        models.signals.post_save.disconnect(self.handle_category_update, sender=Item)
        models.signals.post_save.disconnect(self.handle_rate_update, sender=Rate)
        models.signals.post_delete.disconnect(self.handle_rate_update, sender=Rate)
        models.signals.post_save.disconnect(self.handle_comment_update, sender=Comment)
        models.signals.post_delete.disconnect(self.handle_comment_update, sender=Comment)

        super(RateOnlySignalProcessor, self).teardown()