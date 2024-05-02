from flask import (
    Blueprint, jsonify, request, session, current_app
)
from ...models import db, User , _PlatformEnum, Organization, OAuth, IGPage, IGBusinessAccount, IGMedia, IGComment, IGThread, IGCustomer
from pathvalidate import replace_symbol
from ....utils import file_utils, IGApiFetcher
from flask_login import login_required, current_user
import traceback

threads_bp = Blueprint('threads', __name__)

def thread_result_obj(at, comment_timestamp, comment_message):
    return {
        "id": at.id,
        "username": at.customer.name,
        "avatar": at.customer.profile_picture_url,
        "platform": _PlatformEnum.Instagram.name,
        "lastUpdated": comment_timestamp,
        "message": comment_message,
        "unread": at.is_read,
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

@threads_bp.route("/", methods=["GET", "POST"])
@login_required
def all_threads():
    try:
        if request.method == "GET":
            
            # pages für den user finden
            pages = db.session.execute(db.select(IGPage).filter_by(user=current_user)).scalars().all()
            
            if len(pages) == 0:
                return jsonify({"error":"No pages associated with user"}), 500
            
            # alle Threads finden
            media_ids = []
            for p in pages:
                for b in p.business_accounts:
                    for m in b.medias:
                        media_ids.append(m.id)
                                  
            oauth = db.session.execute(db.select(OAuth).filter(OAuth.user.has(id=current_user.id))).scalar_one_or_none()
            
            query_offset = request.args.get("offset") if request.args.get("offset") is not None else 0  
            IGApiFetcher.updateInteractions(oauth.token["access_token"], media_ids, query_offset)
            associated_threads = db.session.execute(db.select(IGThread).filter(IGThread.media_id.in_(media_ids))).scalars().all()
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

@threads_bp.route("/<id>", methods=["GET"])
@login_required
def get_messages_by_threadid(id):
    try:
        pages = db.session.execute(db.select(IGPage).filter_by(user=current_user)).scalars().all()
        
        # pages für den user finden
        pages = db.session.execute(db.select(IGPage).filter_by(user=current_user)).scalars().all()
        
        if len(pages) == 0:
            return jsonify({"error":"No pages associated with user"}), 500
        
        # alle Threads finden
        media_ids = []
        for p in pages:
            for b in p.business_accounts:
                for m in b.medias:
                    media_ids.append(m.id)
            
        
        associated_threads = db.session.execute(db.select(IGThread).filter(IGThread.media_id.in_(media_ids)).filter(IGThread.id == id)).scalars().all()
        if len(associated_threads) == 0:
            return jsonify([]), 204
        
        results = []
        for at in associated_threads:
            for com in at.comments:
                results.append(message_result_obj(com))
        
        return jsonify(results), 200
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occoured"}), 500