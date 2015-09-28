from django.test import TestCase

# Create your tests here.

import factory
from products import models
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
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


users = UserFactory.build_batch(10000, first_name="Joe")
items = ItemFactory.create()

print([user.first_name for user in users])
# print([item.name for item in items])

name = factory.Sequence(lambda n: 'item-{0}'.format(n))
price = factory.Sequence(lambda n: '123-{0}'.format(n))
image_url = 'https://github.com/jeezybrick/products_light'
description = '1ddddddddddddddddddddddddddddddddddddddddddddddddddddddd23'


#/////////////////////////////////////////////////////////
i = 0
while i < 1000:

    item = models.Item.objects.create(name='PC', price=11111, image_url='https://github.com/jeezybrick/products_light',
                                      description='1ddddddddddddddddddddddddddddddddddddddddddddddddddddddd23')
    item.save()
    print('item saved!')
    i += 1