__author__ = 'user'
from .models import Category, Item, Rate,Comment
from .cache import ProductCache, CategoryCache, RateCache, CommentCache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.db import models
from haystack import signals
# from haystack.management.commands import update_index
from products.search_indexes import ItemIndex

invalidate_signals = [post_delete, post_save]


@receiver(invalidate_signals, sender=Category)
def invalidate_category(sender, instance, **kwargs):
    CategoryCache().invalidate()


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

    #@receiver(post_save, sender=Rate)
    def handle_rate_change(self, sender, instance, **kwargs):
        print('handle work')
        if instance.item.rates:
            print('if work')
            super(RateOnlySignalProcessor, self).handle_save(
                Item, instance.item.rates, **kwargs
            )

    def setup(self, **kwargs):
        models.signals.post_save.connect(self.handle_save, sender=Item)
        # models.signals.post_save.connect(self.handle_rate_change, sender=Item)
        models.signals.post_delete.connect(self.handle_delete, sender=Item)

    def teardown(self):
        models.signals.post_save.disconnect(self.handle_save, sender=Item)
        models.signals.post_delete.disconnect(self.handle_delete, sender=Item)

'''
@receiver(post_save, sender=Comment)
@receiver(post_save, sender=Rate)
def reindex_mymodel(sender, **kwargs):
    ItemIndex().update()
'''

'''
#hard reset index
@receiver(post_save, sender=Rate)
def UpdateItemIndex(sender, instance, **kwargs):
    update_index.Command().handle()
'''