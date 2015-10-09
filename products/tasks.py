

import datetime
from celery.task import periodic_task
from products.models import Action


"""Delete action if period_to > now()"""


@periodic_task(run_every=60)  # Every 60 seconds
def delete_action():
    Action.objects.filter(period_to__lt=datetime.datetime.now()).delete()
