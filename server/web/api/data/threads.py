from flask import (
    Blueprint, jsonify, request, session, current_app
)
from ...models import db, User , _PlatformEnum, Organization, OAuth, IGPage, IGBusinessAccount, IGMedia, IGComment, IGThread, IGCustomer
from pathvalidate import replace_symbol
from ....utils import file_utils, IGApiFetcher
from flask_login import login_required, current_user
import traceback, requests
from urllib.parse import quote

threads_bp = Blueprint('threads', __name__)

_URL = "https://graph.facebook.com/v19.0"

def thread_result_obj(at, comment_timestamp, comment_message):
    return {
        "id": at.id,
        "username": at.customer.name,
        "avatar": at.customer.profile_picture_url,
        "platform": _PlatformEnum.Instagram.name,
        "lastUpdated": comment_timestamp,
        "message": comment_message,
        "unread": at.is_unread,
        "interactions": len(at.comments)
    }

def message_result_obj(comment):
    return {
        "id": comment.id,
        "threadId": comment.thread_id,
        "message": comment.text,
        "from": comment.customer_id,
        "messageDate": comment.timestamp
    }

def getThreadsByUser(user):
    # pages für den user finden
    pages = db.session.execute(db.select(IGPage).filter_by(user=user)).scalars().all()
    media_ids = []
    for p in pages:
        for b in p.business_accounts:
            for m in b.medias:
                media_ids.append(m.id)
    
    # alle Threads finden            
    threads = db.session.execute(db.select(IGThread).filter(IGThread.media_id.in_(media_ids))).scalars().all()
    return threads

def isThreadByUser(threadId, user):
    return (next((t for t in getThreadsByUser(user) if t.id == threadId), None) != None)

@threads_bp.route("/", methods=["GET", "POST"])
@login_required
def all_threads():
    try:
        if request.method == "GET":         
            oauth = db.session.execute(db.select(OAuth).filter(OAuth.user.has(id=current_user.id))).scalar_one_or_none()
            
            #query_offset = request.args.get("offset") if request.args.get("offset") is not None else 0  
            #IGApiFetcher.updateInteractions(oauth.token["access_token"], media_ids, query_offset)
            associated_threads = getThreadsByUser(current_user)
            if len(associated_threads) == 0:
                return jsonify([]), 204
            
            # Response Objekt bauen, thread um Customer Daten und letzte aktuelle message des Threads + lastUpdated (= zeitpunkt der letzten aktuellen message)
            results = []
            for at in associated_threads:
                last_comment = sorted(at.comments, key=lambda x: x.timestamp)[-1]
                results.append(thread_result_obj(at, last_comment.timestamp, last_comment.text))
            
            sorting_option = request.args.get("sorting") 
            
            if sorting_option == "new" or sorting_option is None:
                results.sort(key=lambda x: x["lastUpdated"])
                results.reverse()
            elif sorting_option == "old":
                results.sort(key=lambda x: x["lastUpdated"])
            elif sorting_option == "most-interaction":
                results.sort(key=lambda x: x["interactions"])
                results.reverse()
            elif sorting_option == "least-interaction":
                results.sort(key=lambda x: x["interactions"])
            else:
                return jsonify({"error":"Unspecified sorting argument, only 'new' (default), 'old', 'most-interaction', 'least-interaction' allowed"}), 500
            return jsonify([r for r in results])
        
        if request.method == "POST":
            # pages für den user finden
            # TODO platform beachten
            pages = db.session.execute(db.select(IGPage).filter_by(user=current_user)).scalars().all()
            
            if len(pages) == 0:
                return jsonify({"error":"No pages associated with user"})

            media_ids = []
            for p in pages:
                for b in p.business_accounts:
                    for m in b.medias:
                        media_ids.append(m.id)
                
            # alle Threads für die posts finden
                # suchsstring anwenden auf IGComment.text
                # pagination anwenden
            stmt = db.select(IGThread).filter(IGThread.media_id.in_(media_ids))
            if "offset" in request.get_json():
                stmt.where(IGThread.id > request.get_json()["offset"])
                
            associated_threads = db.session.execute(stmt).scalars().all()
            if len(associated_threads) == 0:
                return jsonify([]), 204
            
            results = []
            for at in associated_threads:            
                last_comment = sorted(at.comments, key=lambda x: x.timestamp)[-1]
                if "q" in request.get_json() and request.get_json()["q"] != "":
                    query = replace_symbol(request.get_json()["q"])
                    for c in at.comments:
                        if query in c.text:
                            results.append(thread_result_obj(at, last_comment.timestamp, last_comment.text))
                else:
                    results.append(thread_result_obj(at, last_comment.timestamp, last_comment.text))
            return jsonify(results), 200
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occoured"}), 500

@threads_bp.route("/<id>", methods=["GET", "PUT"])
@login_required
def get_messages_by_threadid(id):
    try:
        if request.method == "GET":                        
            associated_threads = getThreadsByUser(current_user)
            if len(associated_threads) == 0:
                return jsonify([]), 204
            
            results = []
            for at in associated_threads:
                for com in at.comments:
                    results.append(message_result_obj(com))
            
            return jsonify(results), 200

        if request.method == "PUT":
            
            associated_threads = getThreadsByUser(current_user)
            
            if len(associated_threads) == 0:
                return jsonify([]), 204
            thread = next((t for t in associated_threads if t.id == int(id)), None)
            
            if thread is None:
                return jsonify({"error":"ID not associated with user account"}), 500
            else:
                if "unread" not in request.get_json():
                    return jsonify({"error", "Illegal unread status"}), 500
                
                status = request.get_json()["unread"]
                
                thread.is_unread = status
                db.session.add(thread)
                db.session.commit()
                return jsonify({}), 200
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occoured"}), 500


@threads_bp.route("/<id>/message", methods=["POST"])
@login_required
def post_message(id):
    try:
        id = int(id)
        body = request.get_json()
        if "message" not in body or body["message"] == "":
            return jsonify({"error": "No message specified"}), 400
        
        if isThreadByUser(id, current_user):
            # Posting
            # /ig-comment-id/replies?message={message}
            thread = db.session.execute(db.select(IGThread).filter(IGThread.id == id)).scalar_one_or_none()
            if thread is None:
                return jsonify({"error": "Thread not associated with user"}), 500
            
            oauth = db.session.execute(db.select(OAuth).filter(OAuth.user.has(id=current_user.id))).scalar_one_or_none()
            print(current_user.organization)
            last_comment = thread.comments[-1]
            res = requests.post(_URL + f"/{last_comment.fb_id}/replies?message={quote(body['message'])}&access_token={oauth.token['access_token']}")
            IGApiFetcher.getComments(oauth.token['access_token'], thread.media)
            # file mit Verbesserungen erweitern
            if "generated_message" in body:
                file_utils.save_corrected_messages(body["generated_message"], body["message"], f'{current_app.config["UPLOAD_FOLDER"]}/{current_user.organization.folder_path}/')
            return jsonify({}), 200
        else:
            return jsonify({"error":"Can't post in thread if thread is not associated with user"}), 500
        
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occoured"}), 500