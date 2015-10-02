# Create your tests here.

import factory
import random
import string
from products import models
from factory.django import DjangoModelFactory


def random_string(length=100):
    return u''.join(random.choice(string.ascii_letters) for x in range(length))


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
    description = factory.LazyAttribute(lambda t: random_string())


users = UserFactory.build_batch(10000, first_name="Joe")
items = ItemFactory.create_batch(1000)

print([user.first_name for user in users])
print([item.description for item in items])

'''
#/////////////////////////////////////////////////////////
i = 0
while i < 1000:

    item = models.Item.objects.create(name='PC', price=11111, image_url='https://github.com/jeezybrick/products_light',
                                      description='1ddddddddddddddddddddddddddddddddddddddddddddddddddddddd23')
    item.save()
    print('item saved!')
    i += 1
'''