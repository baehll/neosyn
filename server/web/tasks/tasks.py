from celery import Celery, shared_task
from celery.signals import task_prerun
from ...db.models import db, OAuth, User, Organization, IGThread, IGComment, IGMedia, OpenAIRun
from ...db import db_handler
from ...social_media_api import IGApiFetcher
from ...utils import assistant_utils
from flask import current_app
from flask_login import current_user
import os

@shared_task
def init_ig_data(user_id, oauth_token):
    db.engine.dispose()

    user = db.session.execute(db.select(User).filter(User.id == user_id)).scalar_one()
    return IGApiFetcher.updateAllEntries(oauth_token["access_token"], user)

@shared_task
def add_interactions_to_vector_store(user_id):
    db.engine.dispose()

    user = db.session.execute(db.select(User).filter(User.id == user_id)).scalar_one()
    # alle replies zu kommentaren finden
    # tupel (kommentar, reply) array bilden 
    # assistant_utils.upload_csv_lines_to_openai("filename", user.organization.vec_storage_id, reply_comments)
@shared_task
def init_assistant(orga_id):
    db.engine.dispose()

    orga = db.session.execute(db.select(Organization).filter(Organization.id == orga_id)).scalar_one()
    return assistant_utils.init_assistant(orga)

@shared_task
def update_interactions(oauth_token, thread_ids):
    db.engine.dispose()

    IGApiFetcher.updateInteractions(oauth_token, thread_ids)
    
@shared_task
def generate_response(threadId, GPTConfig):
    db.engine.dispose()
    thread = db.session.execute(db.select(IGThread).filter(IGThread.id == threadId)).scalar_one_or_none()
    
    # checken, ob IGMedia vom thread gpt_thread hat
    if thread.media.gpt_thread_id is None:
        gpt_thread = GPTConfig().CLIENT.beta.threads.create(
            tool_resources={
                "file_search": {
                    "vector_store_ids": [current_user.organization.vec_storage_id]
                }
            }
        )
    else:
        gpt_thread = GPTConfig().CLIENT.beta.threads.retrieve(thread.media.gpt_thread_id)
    
    thread.media.gpt_thread_id = gpt_thread.id
    db_handler.commitAllToDB([thread])
    
    # Überprüfen, ob in metadata der aktuellste kommentar steht
    if "last_comment_id" not in gpt_thread.metadata:
        latest_comments = thread.media.comments
    else:
        latest_comments = db.session.execute(db.select(IGComment).join(IGMedia).filter(IGComment.id > int(gpt_thread.metadata["last_comment_id"])).filter(IGMedia == thread.media)).scalars()
    
    last_id = None
    # Alle Kommentare in diesem Thread hinzufügen
    for c in latest_comments:
        if len(c.customer.bz_acc) == 1:
            text = "Von User: " 
        else:
            text = "Von Customer: "
        text += c.text
        message = GPTConfig().CLIENT.beta.threads.messages.create(
            thread_id=gpt_thread.id,
            role="user",
            content=text
        )
        last_id = c.id
    
    if last_id is not None:
        GPTConfig().CLIENT.beta.threads.update(
            gpt_thread.id,
            metadata={
                "last_comment_id":str(last_id)
            })        
        
    # Platzhalter aus den den instructions mit media Informationen ersetzen
    instructions = open(os.path.join(current_app.config["CONFIG_FOLDER"], "instruction_template.txt"),"r", encoding="utf-8").read()   
    instructions = instructions.replace("{{caption}}", thread.media.caption).replace("{{thumbnail}}", thread.media.media_url).replace("{{company_name}}", current_user.organization.name)
    # Antworten Generieren     
    run = GPTConfig().CLIENT.beta.threads.runs.create_and_poll(
        thread_id=gpt_thread.id,
        assistant_id=current_app.config["GPT_ASSISTANT_ID"],
        instructions=instructions
    )
    db_run = OpenAIRun(run_id=run.id, organization=current_user.organization)
    
    db_handler.commitAllToDB([db_run])
    return run, gpt_thread