__author__ = 'user'

import factory
from products import models


class UserFactory(factory.Factory):
    class Meta:
        model = models.User

    first_name = 'John'
    last_name = 'Doe'
    admin = False


users = UserFactory.build_batch(10, first_name="Joe")

print([user.first_name for user in users])