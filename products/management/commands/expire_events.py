__author__ = 'user'

import datetime
from django.core.management.base import NoArgsCommand
from products.models import Action


class Command(NoArgsCommand):

    help = 'Expires event objects which are out-of-date'

    def handle_noargs(self):
        Action.objects.filter(period_to__lt=datetime.datetime.now()).delete()