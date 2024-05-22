from celery import Celery, shared_task
from ..models import db, OAuth, User, Organization
from ...utils import IGApiFetcher
from ...utils import assistant_utils

@shared_task
def init_ig_data(user_id, oauth_token):
    user = db.session.execute(db.select(User).filter(User.id == user_id)).scalar_one()
    return IGApiFetcher.updateAllEntries(oauth_token["access_token"], user)

@shared_task
def init_assistant(orga_id):
    orga = db.session.execute(db.select(Organization).filter(Organization.id == orga_id)).scalar_one()
    return assistant_utils.init_assistant(orga)

@shared_task
def update_interactions(oauth_token, thread_ids):
    IGApiFetcher.updateInteractions(oauth_token, thread_ids)