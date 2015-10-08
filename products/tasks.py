__author__ = 'user'

import datetime
from celery.task import periodic_task
from products.models import Action


@periodic_task(run_every=10)
def myfunc():
    print('TASK WORK')
    Action.objects.filter(period_to__lt=datetime.datetime.now()).delete()
