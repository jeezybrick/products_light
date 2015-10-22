__author__ = 'user'

import factory
import random
import string
from django.core.management.base import BaseCommand
from products import models
from my_auth.models import MyUser


def random_string(length=100):
    return u''.join(random.choice(string.ascii_letters) for x in range(length))


def random_int(fromm, to):
    return random.randint(fromm, to)


def random_image_url():
    choice = ['', 'http://i.imgur.com/55ypmZX.jpg']
    return random.choice(choice)

# count of objects
count_of_users = 10
count_of_parent_categories = 10
count_of_sub_categories = 50
count_of_items = 100
count_of_comments = 50


class Command(BaseCommand):

    """Create users"""
    class UserFactory(factory.Factory):
        class Meta:
            model = MyUser

        username = factory.LazyAttribute(lambda t: random_string(length=10))
        email = factory.LazyAttribute(lambda t: random_string(length=10)+'@gmail.com')
        password = factory.LazyAttribute(lambda t: random_string(length=10))

    users = UserFactory.create_batch(count_of_users)
    print('Wait.Users created...')
    [user.save() for user in users]

    """Create parent categories"""
    class ParentCategoryFactory(factory.Factory):
        class Meta:
            model = models.Category

        name = factory.LazyAttribute(lambda t: random_string(length=10))
        parent_category_id = None

    categories = ParentCategoryFactory.create_batch(count_of_parent_categories)
    print('Wait.Parent categories created...')
    [category.save() for category in categories]

    """Create sub categories"""
    class SubCategoryFactory(factory.Factory):
        class Meta:
            model = models.Category

        name = factory.LazyAttribute(lambda t: random_string(length=10))
        """Range of exiting id's parent_category"""
        parent_category_id = factory.LazyAttribute(lambda t: random_int(1, count_of_parent_categories))

    categories = SubCategoryFactory.create_batch(count_of_sub_categories)
    print('Wait.Sub categories created...')
    [category.save() for category in categories]

    """Create items"""
    class ItemFactory(factory.Factory):
        class Meta:
            model = models.Item

        name = factory.Sequence(lambda n: 'item-{0}'.format(n))
        price = factory.LazyAttribute(lambda t: random_int(1, 10000))
        image_url = factory.LazyAttribute(lambda t: random_image_url())
        description = factory.LazyAttribute(lambda t: random_string())
        user_id = factory.LazyAttribute(lambda t: random_int(1, count_of_users))
        quantity = factory.LazyAttribute(lambda t: random_int(0, 50))

    items = ItemFactory.create_batch(count_of_items)
    print('Wait.Items created...')
    [item.save() for item in items]

    """Create comments"""
    class CommentFactory(factory.Factory):
        class Meta:
            model = models.Comment

        username = factory.LazyAttribute(lambda t: random_string(length=10))
        message = factory.LazyAttribute(lambda t: random_string())
        """Range of exiting id's items"""
        item_id = factory.LazyAttribute(lambda t: random_int(1, count_of_items))

    comments = CommentFactory.create_batch(count_of_comments)
    print('Wait.Comments created...')
    [comment.save() for comment in comments]

    def handle(self, *args, **options):
        pass
