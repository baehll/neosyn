from celery import Celery, shared_task
from ..models import db
from ...utils import IGApiFetcher
import time

@shared_task
def add(x,y):
    time.sleep(60)
    return x+y