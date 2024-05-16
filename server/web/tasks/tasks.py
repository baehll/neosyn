from celery import Celery, shared_task
from ..models import db, OAuth
from ...utils import IGApiFetcher
from ...utils import assistant_utils

@shared_task
def init_ig_data(user):
    oauth = db.session.execute(db.select(OAuth).filter(OAuth.user.has(id=user.id))).scalar_one_or_none()
    return IGApiFetcher.updateAllEntries(oauth.token["access_token"], user)

@shared_task
def init_assistant(orga):
    return assistant_utils.init_assistant(orga)

@shared_task
def update_interactions(user):
    pass

# bestehende Interaktionen sammeln