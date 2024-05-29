from flask import (
    Blueprint, jsonify, request, session, current_app
)

from ....social_media_api import IGApiFetcher
from ....db.models import db, _PlatformEnum, OAuth, IGPage, IGThread, AnswerImprovements, IGCustomer, IGBusinessAccount, IGMedia
from ....db import db_handler
from pathvalidate import replace_symbol
from ....utils import file_utils
from flask_login import login_required, current_user
import traceback, requests
from urllib.parse import quote
from zoneinfo import ZoneInfo
from ...tasks import update_interactions

threads_bp = Blueprint('threads', __name__)

_URL = "https://graph.facebook.com/v19.0"

def thread_result_obj(at, comment):
    return {
        "id": at.id,
        "username": at.customer.name,
        "avatar": at.customer.profile_picture_url,
        "platform": _PlatformEnum.Instagram.name,
        "lastUpdated": comment.timestamp.astimezone(ZoneInfo("Europe/Berlin")),
        "message": comment.text,
        "unread": at.is_unread,
        "interactions": len(at.comments),
        "bookmarked": at.is_bookmarked
    }


def serialize_comment(comment, bzaccs):
    result = {
        "id": comment.id,
        "threadId": comment.thread_id,
        "message": comment.text,
        "messageDate": comment.timestamp.astimezone(ZoneInfo("Europe/Berlin")),
        "from": comment.customer.id
    }
    
    # Wenn das Kommentar mit einem Business Account verfasst wurde, der zum User gehört
    if len(comment.customer.bz_acc) > 0 and comment.customer.bz_acc[0] in bzaccs:
        result["from"] = None
        
    return result

def getThreadsByUser(user):
    # pages für den user finden
    threads = []
    for p in user.pages:
        for b in p.business_accounts:
            threads.extend(b.threads)
    return threads

def isThreadByUser(threadId, user):
    # current_user -> pages -> bzaccs -> medias -> threads
    stmt = db.select(IGThread).join(IGMedia).join(IGBusinessAccount).join(IGPage).filter(IGPage.user==user).filter(IGThread.id==threadId)
    thread = db.session.execute(stmt).scalar_one_or_none()
    return (thread is not None)

@threads_bp.route("/", methods=["GET", "POST"])
@login_required
def all_threads():
    try:        
        if len(current_user.pages) == 0:
            return jsonify({"error":"No pages associated with user"}), 500

        media_ids = []
        for p in current_user.pages:
            for b in p.business_accounts:
                for m in b.medias:
                    media_ids.append(m.id)
        
        # Offset Query Parameter     
        offset = int(request.args.get("offset")) if request.args.get("offset") is not None else 1
        print(offset)
        # current_user -> page -> bzacc -> medias -> threads, limit 20, offset
        stmt = db.select(IGThread).join(IGMedia).join(IGBusinessAccount).join(IGPage).filter(IGPage.user == current_user).limit(20).offset(offset)
        #stmt = db.select(IGThread).filter(IGThread.media_id.in_(media_ids)).limit(20).offset((offset - 1) * 20)
        print(stmt)
        associated_threads = db.session.execute(stmt).scalars().all()
        
        if len(associated_threads) == 0:
            return jsonify([]), 204
        
        #print(len(associated_threads))
        # Post Body Query
        threads = []
        for at in associated_threads:       
            if len(at.comments) == 0:
                db_handler.deleteFromDB([at])
                continue
            
            last_comment = sorted(at.comments, key=lambda x: x.timestamp)[-1]
            if "q" in request.get_json() and request.get_json()["q"] != "":
                query = replace_symbol(request.get_json()["q"])
                for c in at.comments:
                    if query in c.text or query in c.customer.name:
                        threads.append((at, last_comment))
                        break
            else:
                threads.append((at, last_comment))    
        
        # Sorting Query Parameter        
        sorting_option = request.args.get("sorting") 
            
        if sorting_option == "new" or sorting_option is None:
            threads.sort(key=lambda x: x[1].timestamp, reverse=True)
        elif sorting_option == "old":
            threads.sort(key=lambda x: x[1].timestamp)
        elif sorting_option == "most_interaction":
            threads.sort(key=lambda x: len(x[0].comments), reverse=True)
        elif sorting_option == "least_interaction":
            threads.sort(key=lambda x: len(x[0].comments))
        else:
            return jsonify({"error":"Unspecified sorting argument, only 'new' (default), 'old', 'most-interaction', 'least-interaction' allowed"}), 500
        
        thread_ids = [t[0].id for t in threads]
        #IGApiFetcher.updateInteractions(oauth.token["access_token"], thread_ids[offset:offset+10])
        
        update_interactions.delay(current_user.oauth.token["access_token"], thread_ids[offset:offset+10])
        if len(thread_ids) > 10:
            if(offset+20 <= len(thread_ids)):
                res = update_interactions.delay(current_user.oauth.token["access_token"], thread_ids[offset+10:offset+20])
                res.forget()
            elif (offset+10 <= len(thread_ids)):
                res = update_interactions.delay(current_user.oauth.token["access_token"], thread_ids[offset+10:])
                res.forget()
        
        results = [thread_result_obj(t[0], t[1]) for t in threads]
        
        return jsonify(results), 200
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occoured"}), 500

@threads_bp.route("/<id>", methods=["GET", "PUT", "DELETE"])
@login_required
def get_messages_by_threadid(id):
    try:
        if request.method == "GET":                        
            pages = db.session.execute(db.select(IGPage).filter_by(user=current_user)).scalars().all()
            media_ids = []
            user_bz_accs = []
            for p in pages:
                for b in p.business_accounts:
                    user_bz_accs.append(b)
                    for m in b.medias:
                        media_ids.append(m.id)
            
            # alle Threads finden            
            thread = db.session.execute(db.select(IGThread)
                                         .filter(IGThread.media_id.in_(media_ids))
                                         .filter_by(id=id)).scalar_one_or_none()
            if thread is None:
                return jsonify(), 204
            
            results = []
            at_comments = sorted(thread.comments, key=lambda x: x.timestamp)
            for com in at_comments:
                results.append(serialize_comment(com, user_bz_accs))
            
            return jsonify(results), 200

        if request.method == "PUT":
            if isThreadByUser(int(id), current_user):
                if "unread" not in request.get_json():
                    return jsonify({"error", "Read status not specified"}), 500
                
                thread = db.session.execute(db.select(IGThread).filter_by(id=int(id))).scalar_one_or_none()
                if thread is not None:
                    status = request.get_json()["unread"]
                    thread.is_unread = status
                    db_handler.commitAllToDB([thread])
                    print(thread)
                    return jsonify(), 200
            else:
                return jsonify({"error":"ID not associated with user account"}), 500
        
        if request.method == "DELETE":
            if isThreadByUser(int(id), current_user):
                thread = db.session.execute(db.select(IGThread).filter(IGThread.id == int(id))).scalar_one_or_none()
                if thread is not None:
                    # TL Kommentar zum Thread suchen
                    tl_comment = next((c for c in thread.comments if c.parent is None), None)
                    if tl_comment is not None:
                        # FB Request für Kommentar löschen
                        #print(f"{_URL}/{tl_comment.fb_id}")
                        
                        req = IGApiFetcher.deleteIGObject(current_user.oauth.token['access_token'], tl_comment.fb_id)
                        if "success" in req.json() and req.json()["success"] == True:
                            db_handler.deleteFromDB(thread.comments)
                            db_handler.deleteFromDB([thread])
                            return jsonify(), 200
                        else:
                            return jsonify({"error":f"Instagram error while deleting, {req.json()['error']['message']}"}), 500
                    else:
                        return jsonify({"error":"Top level comment for thread not found"}), 500
                else:
                    return jsonify({"error":f"Thread with id {id} not found"}), 500
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occoured"}), 500

@threads_bp.route("/<id>/post", methods=["GET"])
@login_required
def get_post_information(id):
    try:
        if not isThreadByUser(int(id), current_user):
            return jsonify(), 204
        
        # jeweiliges media objekt raussuchen und zurückgeben
        thread = db.session.execute(db.select(IGThread).filter(IGThread.id == id)).scalar_one_or_none()
        
        if thread is None:
            return jsonify({"error":"No thread with the specified ID found"})

        return jsonify({
            "id": thread.media.id,
            "threadId": thread.id,
            "permalink": thread.media.permalink,
            "mediaType": thread.media.media_type,
            "postMedia": thread.media.media_url,
            "postContent": thread.media.caption,
            "platform": _PlatformEnum.Instagram.name,
            "likes": thread.media.like_count,
            "comments": thread.media.comments_count,
            "shares": None,
            "timestamp": thread.media.timestamp
        }), 200
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
            
            #print(current_user.organization)
            last_comment = thread.comments[-1]
            res = IGApiFetcher.postReplyToComment(current_user.oauth.token["access_token"], last_comment.fb_id, body['message'])
            IGApiFetcher.getComments(current_user.oauth.token['access_token'], thread.media)
            
            # tabelle mit Verbesserungen erweitern
            if "generated_message" in body:
                improvement = AnswerImprovements(generated_answer=body["generated_message"], improved_answer=body["message"], user=current_user, thread=thread)
                db.session.add(improvement)
                db.session.commit()
            return jsonify(), 200
        else:
            return jsonify({"error":"Can't post in thread if thread is not associated with user"}), 500
        
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occoured"}), 500
    
@threads_bp.route("/bookmarks", methods=["GET"])
@login_required
def get_bookmarked_threads():
    try:
        # pages für den user finden
        pages = db.session.execute(db.select(IGPage).filter_by(user=current_user)).scalars().all()
        media_ids = []
        for p in pages:
            for b in p.business_accounts:
                for m in b.medias:
                    media_ids.append(m.id)
        
        # alle Threads finden  
        stmt = db.select(IGThread).filter(IGThread.media_id.in_(media_ids)).filter_by(is_bookmarked=True).limit(20)
        if request.args.get("offset"):
            try:
                stmt.offset((int(request.args.get("offset")) - 1) * 20)
            except Exception:
                return jsonify({"error" : "Offset is not a number"}), 500
        threads = db.session.execute(stmt).scalars().all()
        # Response Objekt bauen, thread um Customer Daten und letzte aktuelle message des Threads + lastUpdated (= zeitpunkt der letzten aktuellen message)
        results = []
        for at in threads:
            last_comment = sorted(at.comments, key=lambda x: x.timestamp)[-1]
            results.append(thread_result_obj(at, last_comment))
            
        return jsonify(results)
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occoured"}), 500

@threads_bp.route("/bookmarks/<threadId>", methods=["PUT"])
@login_required
def update_bookmarks(threadId):
    try:
        if request.method == "PUT":
            pages = db.session.execute(db.select(IGPage).filter_by(user=current_user)).scalars().all()
            media_ids = []
            for p in pages:
                for b in p.business_accounts:
                    for m in b.medias:
                        media_ids.append(m.id)
            
            # alle Threads finden            
            thread = db.session.execute(db.select(IGThread)
                                         .filter(IGThread.media_id.in_(media_ids))
                                         .filter_by(id=int(threadId))).scalar_one_or_none()
            if thread is None:
                return jsonify({"error":"Thread ID not associated with user"}), 500
            
            if "bookmarked" not in request.get_json():
                return jsonify({"error", "Illegal bookmarked status"}), 500
            
            thread.is_bookmarked = request.get_json()["bookmarked"]
            db.session.add(thread)
            db.session.commit()
            return jsonify(), 200
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occoured"}), 500
