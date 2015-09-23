from django.test import TestCase

# Create your tests here.

import factory
from products import models


class UserFactory(factory.Factory):
    class Meta:
        model = models.User

    first_name = 'John'
    last_name = 'Doe'


class ItemFactory(factory.Factory):
    class Meta:
        model = models.Item

    name = factory.Sequence(lambda n: 'item-{0}'.format(n))
    price = factory.Sequence(lambda n: '123-{0}'.format(n))
    image_url = 'https://github.com/jeezybrick/products_light'
    description = '1ddddddddddddddddddddddddddddddddddddddddddddddddddddddd23'


users = UserFactory.build_batch(1000000, first_name="Joe")
items = ItemFactory.build_batch(10000000000)

print([user.first_name for user in users])
print([item.name for item in items])