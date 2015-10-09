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


def random_parent():
    choice = [1, '']
    return random.choice(choice)


class Command(BaseCommand):

    """Create users"""
    class UserFactory(factory.Factory):
        class Meta:
            model = models.MyUser

        username = factory.LazyAttribute(lambda t: random_string(length=10))
        email = factory.LazyAttribute(lambda t: random_string()+'@gmail.com')
        password = factory.LazyAttribute(lambda t: random_string(length=10))

    users = UserFactory.create_batch(10)
    print('Wait.Users create...')
    [user.save() for user in users]

    """Create paent categories"""
    class ParentCategoryFactory(factory.Factory):
        class Meta:
            model = models.Category

        name = factory.LazyAttribute(lambda t: random_string(length=10))
        parent_category_id = None

    categories = ParentCategoryFactory.create_batch(10)
    print('Wait.Parent categories create...')
    [category.save() for category in categories]

    """Create sub categories"""
    class SubCategoryFactory(factory.Factory):
        class Meta:
            model = models.Category

        name = factory.LazyAttribute(lambda t: random_string(length=10))
        """Range of exiting id's parent_category"""
        parent_category_id = factory.LazyAttribute(lambda t: random_price(254, 262))

    categories = SubCategoryFactory.create_batch(50)
    print('Wait.Sub categories create...')
    [category.save() for category in categories]

    """Create items"""
    class ItemFactory(factory.Factory):
        class Meta:
            model = models.Item

        name = factory.Sequence(lambda n: 'item-{0}'.format(n))
        price = factory.LazyAttribute(lambda t: random_price(1, 10000))
        image_url = factory.LazyAttribute(lambda t: 'https://' + random_string() + '/' + random_string() + '/')
        description = factory.LazyAttribute(lambda t: random_string())
        user_id = 1
        quantity = factory.LazyAttribute(lambda t: random_price(0, 50))

    items = ItemFactory.create_batch(100)
    print('Wait.Items create...')
    [item.save() for item in items]

    """Create comments"""
    class CommentFactory(factory.Factory):
        class Meta:
            model = models.Comment

        username = factory.LazyAttribute(lambda t: random_string(length=10))
        message = factory.LazyAttribute(lambda t: random_string())
        """Range of exiting id's items"""
        item_id = factory.LazyAttribute(lambda t: random_price(5, 50))

    comments = CommentFactory.create_batch(100)
    print('Wait.Comments create...')
    [comment.save() for comment in comments]

    def handle(self, *args, **options):
        pass
