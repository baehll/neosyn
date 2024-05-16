from flask import Blueprint, jsonify, request, current_app
from .models import db, IGPage, IGMedia, IGBusinessAccount, IGComment, OAuth
from ..utils.IGApiFetcher import getPages, getComments, getBusinessAccounts, getMedia, updateAllEntries
from flask_login import current_user, login_required


test = Blueprint('test', __name__)

def GPTConfig():
    from server import GPTConfig
    return GPTConfig

def GPTConfig():
    from server import GPTConfig
    return GPTConfig

def GPTConfig():
    from server import GPTConfig
    return GPTConfig

@test.route("/pages", methods=["GET"])
@login_required
def pages():

    oauth = db.session.execute(db.select(OAuth).filter(OAuth.user.has(id=current_user.id))).scalar_one_or_none()
    results = getPages(oauth.token["access_token"], current_user)
    return jsonify({"results": [r.to_dict() for r in results]})

@test.route("/bz_acc", methods=["POST"])
@login_required
def bz_acc():
    oauth = db.session.execute(db.select(OAuth).filter(OAuth.user.has(id=current_user.id))).scalar_one_or_none()
    page_ids = request.get_json()["pages"]
    pages = db.session.execute(db.select(IGPage).filter(IGPage.fb_id.in_(page_ids))).scalars()
    results = []
    for p in pages:
        results.extend(getBusinessAccounts(oauth.token["access_token"], p))
    return jsonify({"results": [r.to_dict() for r in results]})

@test.route("/medias", methods=["POST"])
@login_required
def medias():
    oauth = db.session.execute(db.select(OAuth).filter(OAuth.user.has(id=current_user.id))).scalar_one_or_none()
    bz_acc_ids = request.get_json()["bz_accs"]
    bz_accs = db.session.execute(db.select(IGBusinessAccount).filter(IGBusinessAccount.fb_id.in_(bz_acc_ids))).scalars()
    results = []
    for b in bz_accs:
        results.extend(getMedia(oauth.token["access_token"], b))
    return jsonify({"results": [r.to_dict() for r in results]})

@test.route("/comments", methods=["POST"])
@login_required
def comments():
    oauth = db.session.execute(db.select(OAuth).filter(OAuth.user.has(id=current_user.id))).scalar_one_or_none()

    media_ids = request.get_json()["medias"]
    medias = db.session.execute(db.select(IGMedia).filter(IGMedia.fb_id.in_(media_ids))).scalars()
    results = []
    for b in medias:
        results.extend(getComments(oauth.token["access_token"], b))
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