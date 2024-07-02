from celery import Celery, shared_task, group, chord
from ...db.models import db, OAuth, User, Organization, IGMedia, OpenAIRun, IGBusinessAccount, IGPage, InteractionExamples
from ...db import db_handler
from ...social_media_api import IGApiFetcher, interaction_query
from ...utils import assistant_utils
from flask import current_app
from flask_login import current_user
from ...cache_config import cache
from rapidfuzz import fuzz
import os, time

@shared_task
def update_ig_entries(user_id):
    #db.engine.dispose()
    user = db.session.execute(db.select(User).filter(User.id == user_id)).scalar_one()
    return IGApiFetcher.updateAllEntries(user.oauth.token["access_token"], user)

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
def fill_media_trees(oauth_token, medias, worker_numbers, id_to_node, media_trees):
    active_tasks = [] 
        
    while medias or active_tasks:
        while medias and len(active_tasks) < worker_numbers:
            media = medias.pop(0)
            task = loadCommentsForMedia.s(oauth_token, media).delay()
            active_tasks.append(task)
        
        for task in active_tasks:
            if task.ready():
                #print(task.result)
                if len(task.result):
                    interaction_query.add_tree(id_to_node, media_trees, task.result)
                active_tasks.remove(task)
        
        time.sleep(0.01)

@shared_task
def get_cached_data(user_id):
    cache_id = f"media_trees_{user_id}"
    return cache.get(cache_id)

@shared_task
def build_cache(user_ids=None):
    #db.engine.dispose()
    
    if user_ids is None:
        users = db.session.execute(db.select(User)).scalars().all()
    else:
        users = db.session.execute(db.select(User).filter(User.id.in_(user_ids))).scalars().all()
        
    #print(user_ids)
    for user in users:
        loadCachedResults.s(user.oauth.token["access_token"], user.id).delay()
    
@shared_task
def presort_cached_results(user_id, option=None):
    print(f"presorting for {user_id}")
    cache_id = f"media_trees_{user_id}"
    cached_data = cache.get(cache_id)
    
    if option is not None:
        cached_data["sorted"][option] = interaction_query.get_sorted_list(cached_data["media_trees"], sort_order=option)
    else:
        if cached_data.get("sorted").get("new") is None:
            cached_data["sorted"]["new"] = interaction_query.get_sorted_list(cached_data["media_trees"])
        if cached_data.get("sorted").get("least_interaction") is None:
            cached_data["sorted"]["least_interaction"] = interaction_query.get_sorted_list(cached_data["media_trees"])

    cache.set(cache_id, cached_data)
    
@shared_task
def loadCachedResults(oauth_token, user_id, updated_media_id=None):
    print(f"loading for {user_id}")
    cache_id = f"media_trees_{user_id}"
    cached_data = cache.get(cache_id)
    
    if cached_data is not None:
        updated_medias = update_ig_entries(user_id)
        if updated_media_id is not None:
            # media tree mit fb_id entfernen aus media trees
            interaction_query.remove_tree(cached_data["id_mapping"], cached_data["media_trees"], updated_media_id)
            # daten für das media objekt sammeln
            task = loadCommentsForMedia.s(oauth_token, updated_media_id).delay()
            while not task.ready():
                time.sleep(0.1)
            # in bestehenden media_trees einsortieren
            interaction_query.add_tree(cached_data["id_mapping"], cached_data["media_trees"], task.result)
        
        fill_media_trees(oauth_token, updated_medias, 2, cached_data["id_mapping"], cached_data["media_trees"])
        return cached_data
    
    # update IGPage, IGBusiness Account und IGMedia für User
    update_ig_entries(user_id)
    
    # für jedes igMedia comments holen und einen forest erstellen, jede kommentar kette ist ein tree
    medias = db.session.execute(db.select(IGMedia).join(IGBusinessAccount).join(IGPage).join(User).filter(User.id == user_id).filter(IGMedia.comments_count > 0).order_by(IGMedia.timestamp.desc()).limit(10)).scalars().all()
    #print(medias)
    media_trees = []
    id_to_node = {}
    
    print(f"starting tasks for {user_id}")
    
    fill_media_trees(oauth_token, [m.fb_id for m in medias], worker_numbers=2, id_to_node=id_to_node, media_trees=media_trees)

    print(f"finished tasks for {user_id}")       
    data = {"media_trees": media_trees, 
            "id_mapping": id_to_node, 
            "sorted":{
                "new": None,
                "least_interaction": None
    }}
       
    cache.set(cache_id, data)

    orga = db.session.execute(db.select(Organization).join(User).filter(User.id == user_id)).scalar_one_or_none()
    if not orga is None and not len(orga.interaction_examples):
        initUserCustomerExamples.s(user_id, media_trees).delay()
    
    presort_cached_results.s(user_id).delay()
    return data
    
@shared_task
def initUserCustomerExamples(user_id, media_trees):
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

def init_gpt_thread(GPTConfig, media, user_id):
    prompt_msg = ""
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
    return prompt_msg, gpt_thread

@shared_task
def generate_response(user_id, GPTConfig, messages):
    db.engine.dispose()
    media = db.session.execute(db.select(IGMedia).filter(IGMedia.fb_id == messages["media"])).scalar_one_or_none()
    prompt_msg = ""
    # checken, ob IGMedia gpt_thread hat
    if media.gpt_thread_id is None:
        prompt_msg, gpt_thread = init_gpt_thread(GPTConfig, media, user_id)
    else:
        gpt_thread = GPTConfig().CLIENT.beta.threads.retrieve(media.gpt_thread_id)
    
    # prompt instructions anhängen
    instructions = open(os.path.join(current_app.config["CONFIG_FOLDER"], "instruction_template.txt"),"r", encoding="utf-8").read()   
    system_instructions = instructions.replace("{{caption}}", media.caption).replace("{{thumbnail}}", media.media_url).replace("{{company_name}}", current_user.organization.name)    
    prompt_msg += "Antworte auf dieses Kommentar "
    
    # letzte Messages aus der Konversation anhängen
    if len(messages["replies"]):
        prompt_msg += f"{messages['replies'][0]['text']}"
    else:
        prompt_msg += f"{messages['text']}"
        
    run = GPTConfig().CLIENT.beta.threads.runs.create_and_poll(
        thread_id=gpt_thread.id,
        assistant_id=current_app.config["GPT_ASSISTANT_ID"],
        instructions=system_instructions,
        additional_messages=[{
            "role": "user",
            "content": prompt_msg
        }]
    )
    db_run = OpenAIRun(run_id=run.id, organization=current_user.organization)
    
    db_handler.commitAllToDB([db_run])
    return run, gpt_thread

@shared_task
def send_posted_message(user_id, GPTConfig, message, media_id):
    db.engine.dispose()
    media = db.session.execute(db.select(IGMedia).filter(IGMedia.id == media_id)).scalar_one_or_none()

    gpt_thread = GPTConfig().CLIENT.beta.threads.retrieve(media.gpt_thread_id)
    prompt_msg = f"User hat folgende Nachricht geschrieben: {message}"
    run = GPTConfig().CLIENT.beta.threads.runs.create(
            thread_id=gpt_thread.id,
            assistant_id=current_app.config["GPT_ASSISTANT_ID"],
            instructions="Berücksichtige diese Nachricht bei der Generierung von neuen Antworten. Generiere hierauf keine Antwort",
            additional_messages=[{"role":"assistant", "content":prompt_msg}]
    )
    db_run = OpenAIRun(run_id=run.id, organization=current_user.organization)
    
    db_handler.commitAllToDB([db_run])
    
def find_similar_words_in_texts(texts, term, threshold=80):
    for text in texts:
        if fuzz.partial_ratio(term, text) >= threshold:
            return True
    return False

def search_term_in_comment(comment, term, threshold=80):
    texts_to_search = [
        comment.get('from', {}).get('username', ''),
        comment.get('text', '')
    ]
    if comment["replies"]:
        for r in comment["replies"]:
            if search_term_in_comment(r, term, threshold):
                return True
    return find_similar_words_in_texts(texts_to_search, term, threshold)
    
@shared_task
def search_for_term_in_cache(trees, term):
    results = []
    for comment in trees:
        if search_term_in_comment(comment, term):
            results.append(comment)
                    
    return results