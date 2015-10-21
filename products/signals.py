
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.db import models
from django.shortcuts import get_object_or_404
from .models import Item, Rate, Comment, Action
from categories.models import Category
from products import cache
from categories.cache import CategoryCache
from haystack import signals
from my_auth.models import MyUser
from my_auth.cache import ShopDetailCache

invalidate_signals = [post_delete, post_save]


@receiver(invalidate_signals, sender=Category)
def invalidate_category(sender, instance, **kwargs):
    CategoryCache().invalidate(parent_category_id__isnull=True)


@receiver(invalidate_signals, sender=Item)
def invalidate_item(sender, instance, **kwargs):
    cache.ProductCache().invalidate(pk=instance.pk)
    # for item-detail
    cache.ProductDetailCache().invalidate(id=str(instance.pk))


@receiver(post_save, sender=Rate)
def invalidate_rate(sender, instance, **kwargs):
    cache.RateCache().invalidate()


@receiver(post_save, sender=Comment)
def invalidate_comment(sender, instance, **kwargs):
    cache.CommentCache().invalidate()


@receiver(post_save, sender=MyUser)
def invalidate_shop(sender, instance, **kwargs):
    ShopDetailCache().invalidate(id=str(instance.pk))


class RateOnlySignalProcessor(signals.RealtimeSignalProcessor):

    def handle_rate_update(self, sender, instance, **kwargs):
        for item in Item.objects.filter(rates__id=instance.id):
            super(RateOnlySignalProcessor, self).handle_save(
                Item, item, **kwargs
            )

    def handle_comment_update(self, sender, instance, **kwargs):
        for item in Item.objects.filter(comments__id=instance.id):
            super(RateOnlySignalProcessor, self).handle_save(
                Item, item, **kwargs
            )

    def handle_category_update(self, sender, instance, **kwargs):
        for item in Item.objects.filter(categories__in=str(instance.id)):
            super(RateOnlySignalProcessor, self).handle_save(
                Item, item, **kwargs
            )

    def handle_action_update(self, sender, instance, **kwargs):
        for item in Item.objects.filter(action=instance.id):
            super(RateOnlySignalProcessor, self).handle_save(
                Item, item, **kwargs
            )

    def handle_category_m2m_update(self, sender, instance, **kwargs):

        item = Item.objects.get(id=instance.id)
        super(RateOnlySignalProcessor, self).handle_save(
                Item, item, **kwargs
            )

    def setup(self, **kwargs):

        models.signals.m2m_changed.connect(self.handle_category_m2m_update, sender=Item.categories.through)
        models.signals.post_save.connect(self.handle_save, sender=Item)
        models.signals.post_delete.connect(self.handle_delete, sender=Item)
        models.signals.post_save.connect(
            self.handle_category_update, sender=Category)
        models.signals.post_delete.connect(
            self.handle_category_update, sender=Category)
        models.signals.post_save.connect(self.handle_rate_update, sender=Rate)
        models.signals.post_delete.connect(
            self.handle_rate_update, sender=Rate)
        models.signals.post_save.connect(
            self.handle_comment_update, sender=Comment)
        models.signals.post_delete.connect(
            self.handle_comment_update, sender=Comment)
        models.signals.post_save.connect(
            self.handle_action_update, sender=Action)
        models.signals.post_delete.connect(
            self.handle_action_update, sender=Action)
        models.signals.post_save.connect(
            self.handle_action_update, sender=MyUser)
        models.signals.post_delete.connect(
            self.handle_action_update, sender=MyUser)

        super(RateOnlySignalProcessor, self).setup()

    def teardown(self):
        models.signals.post_save.disconnect(self.handle_save, sender=Item)
        models.signals.post_delete.disconnect(self.handle_delete, sender=Item)
        models.signals.post_save.disconnect(
            self.handle_category_update, sender=Category)
        models.signals.post_delete.disconnect(
            self.handle_category_update, sender=Category)
        models.signals.post_save.disconnect(
            self.handle_rate_update, sender=Rate)
        models.signals.post_delete.disconnect(
            self.handle_rate_update, sender=Rate)
        models.signals.post_save.disconnect(
            self.handle_comment_update, sender=Comment)
        models.signals.post_delete.disconnect(
            self.handle_comment_update, sender=Comment)
        models.signals.post_save.disconnect(
            self.handle_action_update, sender=Action)
        models.signals.post_delete.disconnect(
            self.handle_action_update, sender=Action)
        models.signals.post_save.disconnect(
            self.handle_action_update, sender=MyUser)
        models.signals.post_delete.disconnect(
            self.handle_action_update, sender=MyUser)

        super(RateOnlySignalProcessor, self).teardown()
