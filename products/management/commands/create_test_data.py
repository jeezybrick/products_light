__author__ = 'user'

import factory
import random
import string
from django.core.management.base import BaseCommand
from products import models


def random_string(length=100):
    return u''.join(random.choice(string.ascii_letters) for x in range(length))


def random_price(fromm, to):
    return random.randint(fromm, to)


class Command(BaseCommand):

    """Create items"""
    class ItemFactory(factory.Factory):
        class Meta:
            model = models.Item

        name = factory.Sequence(lambda n: 'item-{0}'.format(n))
        price = factory.LazyAttribute(lambda t: random_price(1, 10000))
        image_url = 'https://github.com/jeezybrick/products_light'
        description = factory.LazyAttribute(lambda t: random_string())

    items = ItemFactory.create_batch(100)
    [item.save() for item in items]

    """Create comments"""
    class CommentFactory(factory.Factory):
        class Meta:
            model = models.Comment

        username = factory.LazyAttribute(lambda t: random_string(length=10))
        message = factory.LazyAttribute(lambda t: random_string())
        """Range of exiting id's items"""
        item_id = factory.LazyAttribute(lambda t: random_price(320, 350))

    comments = CommentFactory.create_batch(100)
    [comment.save() for comment in comments]

    def handle(self, *args, **options):
        pass
