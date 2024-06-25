from celery import Celery, shared_task, group, chord
from ...db.models import db, OAuth, User, Organization, IGMedia, OpenAIRun, IGBusinessAccount, IGPage, InteractionExamples
from ...db import db_handler
from ...social_media_api import IGApiFetcher, interaction_query
from ...utils import assistant_utils
from flask import current_app
from flask_login import current_user
import os, time

@shared_task
def init_ig_data(user_id, oauth_token):
    db.engine.dispose()

    user = db.session.execute(db.select(User).filter(User.id == user_id)).scalar_one()
    return IGApiFetcher.updateAllEntries(oauth_token, user)

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
def loadCommentsForMedia(oauth_token, media_fb_id):
    return IGApiFetcher.getLatestComments(oauth_token, media_fb_id) 

@shared_task
def loadCachedResults(oauth_token, cache_id, user_id, updated_media_id=None):
    db.engine.dispose()
    
    cached_data = current_app.extensions["cache"].get(cache_id)

    #print(f"test caching {cache_id}")
    if cached_data is not None:
        if updated_media_id is not None:
            # media tree mit fb_id entfernen aus media trees
            interaction_query.remove_tree(cached_data["id_mapping"], cached_data["media_trees"], updated_media_id)
            # daten für das media objekt sammeln
            task = loadCommentsForMedia.s(oauth_token, updated_media_id).delay()
            while not task.ready():
                time.sleep(0.1)
            # in bestehenden media_trees einsortieren
            interaction_query.add_tree(cached_data["id_mapping"], cached_data["media_trees"], task.result)
        return cached_data
    
    # update IGPage, IGBusiness Account und IGMedia für User
    init_ig_data.delay(user_id, oauth_token)
    
    # für jedes igMedia comments holen und einen forest erstellen, jede kommentar kette ist ein tree
    medias = db.session.execute(db.select(IGMedia).join(IGBusinessAccount).join(IGPage).join(User).filter(User.id == user_id).order_by(IGMedia.timestamp.desc()).limit(10)).scalars().all()
    active_tasks = []
    
    media_trees = []
    id_to_node = {}
    
    print("starting tasks")
    while medias or active_tasks:
        while medias and len(active_tasks) < 2:
            media = medias.pop(0)
            task = loadCommentsForMedia.s(oauth_token, media.fb_id).delay()
            active_tasks.append(task)
        
        for task in active_tasks:
            if task.ready():
                if len(task.result):
                    interaction_query.add_tree(id_to_node, media_trees, tuple(task.result))
                active_tasks.remove(task)
        
        time.sleep(0.01)
    print("finished tasks")         
    data = {"media_trees": media_trees, "id_mapping": id_to_node}
       
    current_app.extensions["cache"].set(cache_id, data)

    orga = db.session.execute(db.select(Organization).join(User).filter(User.id == user_id)).scalar_one_or_none()
    if not orga is None and not len(orga.interaction_examples):
        initUserCustomerExamples.s(oauth_token, user_id, media_trees).delay()
    
    return data

@shared_task
def initUserCustomerExamples(oauth_token, user_id, media_trees):
    db.engine.dispose()
    results = []
    bzacc = db.session.execute(db.select(IGBusinessAccount).join(IGPage).join(User).filter(User.id == user_id)).scalar_one_or_none()
    for tree in media_trees:
        for node in tree[1]:
            for r in node["replies"]:
                if r["from"]["id"] == bzacc.fb_id:
                    results.append(InteractionExamples(customer_msg=node["text"], user_msg=r["text"]))
        if len(results) >= 5:
            break
    #print(results)
    db_handler.commitAllToDB(results)
    orga = db.session.execute(db.select(Organization).join(User).filter(User.id == user_id)).scalar_one_or_none()
    orga.interaction_examples = results
    db_handler.commitToDB(orga)
  
@shared_task
def generate_response(user_id, media_id, GPTConfig, messages):
    db.engine.dispose()
    media = db.session.execute(db.select(IGMedia).filter(IGMedia.fb_id == messages["media"])).scalar_one_or_none()
    prompt_msg = ""
    # checken, ob IGMedia gpt_thread hat
    if media.gpt_thread_id is None:
        gpt_thread = GPTConfig().CLIENT.beta.threads.create(
            tool_resources={
                "file_search": {
                    "vector_store_ids": [current_user.organization.vec_storage_id]
                }
            }
        )
        media.gpt_thread_id = gpt_thread.id
        db_handler.commitAllToDB([media])
        # wenn interaction examples existieren, bis zu 10 davon an eine message hängen
        interaction_examples = db.session.execute(db.select(InteractionExamples).join(Organization).join(User).filter(User.id == user_id).limit(10)).scalars().all()
    
        for ex in interaction_examples:
            prompt_msg += ex.export()
    else:
        gpt_thread = GPTConfig().CLIENT.beta.threads.retrieve(media.gpt_thread_id)
    
    # prompt instructions anhängen
    instructions = open(os.path.join(current_app.config["CONFIG_FOLDER"], "instruction_template.txt"),"r", encoding="utf-8").read()   
    prompt_msg += instructions.replace("{{caption}}", media.caption).replace("{{thumbnail}}", media.media_url).replace("{{company_name}}", current_user.organization.name)    
    prompt_msg += "Antworte auf dieses Kommentar "
    # letzte Messages aus der Konversation anhängen
    if len(messages["replies"]):
        prompt_msg += f"{messages['replies'][0]['text']}"
    else:
        prompt_msg += f"{messages['text']}"
        
    run = GPTConfig().CLIENT.beta.threads.runs.create_and_poll(
        thread_id=gpt_thread.id,
        assistant_id=current_app.config["GPT_ASSISTANT_ID"],
        instructions=prompt_msg
    )
    db_run = OpenAIRun(run_id=run.id, organization=current_user.organization)
    
    db_handler.commitAllToDB([db_run])
    return run, gpt_thread