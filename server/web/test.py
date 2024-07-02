from flask import Blueprint, jsonify, request, current_app
from ..db.models import db, IGPage, IGMedia, IGBusinessAccount, OAuth
from ..social_media_api.IGApiFetcher import getPages, getBusinessAccounts, getMedia, updateAllEntries
from flask_login import current_user, login_required
from .tasks import update_ig_entries, loadCachedResults, get_cached_data
from datetime import datetime
from zoneinfo import ZoneInfo
from ..cache_config import cache
test = Blueprint('test', __name__)

def GPTConfig():
    from server import GPTConfig
    return GPTConfig

@test.route("/pages", methods=["GET"])
@login_required
def pages():
    results = getPages(current_user.oauth.token["access_token"], current_user)
    return jsonify({"results": [r.to_dict() for r in results]})

@test.route("/bz_acc", methods=["POST"])
@login_required
def bz_acc():
    page_ids = request.get_json()["pages"]
    pages = db.session.execute(db.select(IGPage).filter(IGPage.fb_id.in_(page_ids))).scalars()
    results = []
    for p in pages:
        results.extend(getBusinessAccounts(current_user.oauth.token["access_token"], p))
    return jsonify({"results": [r.to_dict() for r in results]})

@test.route("/medias", methods=["POST"])
@login_required
def medias():
    bz_acc_ids = request.get_json()["bz_accs"]
    bz_accs = db.session.execute(db.select(IGBusinessAccount).filter(IGBusinessAccount.fb_id.in_(bz_acc_ids))).scalars()
    results = []
    for b in bz_accs:
        results.extend(getMedia(current_user.oauth.token["access_token"], b))
    return jsonify({"results": [r.to_dict() for r in results]})

@test.route("/update_all_entries", methods=["GET"])
@login_required
def update_all_entries():
    oauth = db.session.execute(db.select(OAuth).filter(OAuth.user.has(id=current_user.id))).scalar_one_or_none()
    updateAllEntries(oauth.token["access_token"], current_user)
    return jsonify({}), 200

@test.route("/thread_run_status/<thread_id>/<run_id>", methods=["GET"])
@login_required
def thread_run_status(thread_id, run_id):
    run = GPTConfig().CLIENT.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    if run.status == "completed":
        messages = GPTConfig().CLIENT.beta.threads.messages.list(thread_id=thread_id)
        print(messages)
        return jsonify(messages)
    else:
        print(run)
        return jsonify(run.status)
    
@test.route("/task", methods=["GET"])
@login_required
def task():
    task = update_ig_entries.delay(current_user.id)
    print(task.backend)
    return jsonify(task.id)

@test.route("/task_status/<id>", methods=["GET"])
@login_required
def task_status(id):
    # task = AsyncResult(id)
    # response = {
    #     'task_id': task.id,
    #     'status': task.status,
    #     'result': task.result if task.status == 'SUCCESS' else None
    # }
    print(datetime.now())
    print(datetime.now().astimezone(ZoneInfo("Europe/Berlin")))
    return jsonify()

# @test.route("/cached_results", methods=["GET"])
# @login_required
# def cached_results():
#     caching_key = f"media_trees_{current_user.id}"
#     task = loadCachedResults.delay(current_user.oauth.token["access_token"], current_user.id).get()
#     return jsonify(task)

@test.route("/cached_results/<id>", methods=["GET"])
@login_required
def cached_results_by_id(id):
    # caching_key = f"media_trees_{id}"
    # print(caching_key)
    # oauth = db.session.execute(db.select(OAuth).filter(OAuth.user.has(id=id))).scalar_one_or_none()
    
    # print(f"access_token: {oauth.token['access_token']}")
    # task = loadCachedResults.delay(oauth.token["access_token"], id).get()
    cached_data = get_cached_data.delay(id).get()
    print(cache.get(f"media_trees_{id}"))
    return jsonify(cached_data)