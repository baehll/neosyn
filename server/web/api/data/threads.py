from flask import (
    Blueprint, jsonify, request
)

from ....social_media_api import IGApiFetcher, interaction_query
from ....db.models import db, _PlatformEnum, IGPage, AnswerImprovements, IGBusinessAccount, IGMedia, User
from ....db import db_handler
from pathvalidate import replace_symbol
from flask_login import login_required, current_user
import traceback
from zoneinfo import ZoneInfo
from ...tasks import update_interactions, loadCachedResults
from dateutil import parser as date_parser

threads_bp = Blueprint('threads', __name__)

def thread_result_obj(comment):
    response = {
        "id": comment["id"],
        "username": comment["from"]["username"],
        "avatar": None,
        "platform": _PlatformEnum.Instagram.name,
        "lastUpdated": None,
        "message": comment["text"],
        "unread": True,
        "interactions": len(comment["replies"]) + 1,
        "bookmarked": False,
        "media": comment["media"]
    }
    timestamp = None
    if len(comment["replies"]):
        timestamp = max(comment["timestamp"], comment["replies"][0]["timestamp"])
    else: 
        timestamp = comment["timestamp"]
    response["lastUpdated"] = date_parser.isoparse(timestamp).astimezone(ZoneInfo("Europe/Berlin"))
    
    return response

def serialize_comment(comment, bzaccs):
    result = {
        "id": comment["id"],
        "threadId": comment["media"],
        "message": comment["text"],
        "messageDate": date_parser.isoparse(comment["timestamp"]).astimezone(ZoneInfo("Europe/Berlin")),
        "from": None
    }
    
    if comment["from"]["id"] not in bzaccs or comment["from"]["id"] != bzaccs:
        result["from"] = comment["from"]["id"]
        
    return result

def sort_threads(sorting_option, threads, offset, slice_length):
    # erst sortierung festlegen
    if sorting_option == "new" or sorting_option is None:
        return interaction_query.get_sorted_slice(threads, interaction_query.traverse_pre_order_gen, offset, offset+slice_length)
    elif sorting_option == "old":
        return interaction_query.get_sorted_slice(threads, interaction_query.traverse_post_order_gen, offset, offset+slice_length)
    #elif sorting_option == "most_interaction":
        #threads.sort(key=lambda x: len(x[0].comments), reverse=True)
    #elif sorting_option == "least_interaction":
        #threads.sort(key=lambda x: len(x[0].comments))

@threads_bp.route("/", methods=["POST"])
@login_required
def all_threads():
    try:        
    #     if len(current_user.pages) == 0:
    #         return jsonify({"error":"No pages associated with user"}), 500
        
        
        
        # Offset Query Parameter     
        offset = int(request.args.get("offset")) if request.args.get("offset") is not None else 0
        unread = request.args.get("unread") if request.args.get("unread") else None

        caching_key = f"media_trees_{current_user.id}"
        cached_data = loadCachedResults.delay(current_user.oauth.token["access_token"], caching_key, current_user.id).get()
        all_threads = interaction_query.convert_lists_to_tuples(cached_data["media_trees"])
        
        if len(all_threads) == 0:
            return jsonify([]), 204
        
        sorting_option = request.args.get("sorting") 
        if sorting_option not in [None, "new", "old", "most_interaction", "least_interaction"]:
            return jsonify({"error":"Unspecified sorting argument, only 'new' (default), 'old', 'most-interaction', 'least-interaction' allowed"}), 500
        
        sorted_threads = sort_threads(sorting_option, all_threads, offset, 25)
        # Nach Begriff filtern
            # erste Slice mit 20 Einträgen
            # durchsuchen nach Begriff in username oder text des Kommentars
            # wenn weniger als 20 Ergebnisse, dann nächste Slice durchsuchen
        if "q" in request.get_json() and request.get_json()["q"] != "":
            query = replace_symbol(request.get_json()["q"])
            i = 1
            filtered_threads = []
            
            while True:
                for t in sorted_threads:
                    if query in t["text"] or query in t["from"]["username"]:
                        filtered_threads.append(thread_result_obj(t))
                    elif "replies" in t:
                        for reply in t["replies"]:
                            if query in reply["text"] or query in reply["from"]["username"]:
                                filtered_threads.append(thread_result_obj(t))
                                break                        
                if len(filtered_threads) >= 25 or len(sorted_threads) < 25:
                    return jsonify(filtered_threads), 200
                else:
                    sorted_threads = sort_threads(sorting_option, all_threads, offset+(25)*i, offset+(25)*(i+1))
                    i += 1
        else:
            return jsonify([thread_result_obj(t) for t in sorted_threads]), 200
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occoured"}), 500

@threads_bp.route("/<id>", methods=["GET", "PUT", "DELETE"])
@login_required
def get_messages_by_threadid(id):
    try:
        caching_key = f"media_trees_{current_user.id}"
        cached_data = loadCachedResults.delay(current_user.oauth.token["access_token"], caching_key, current_user.id).get()
        bzaccs = db.session.execute(db.select(IGBusinessAccount.fb_id).join(IGPage).join(User).filter(User.id == current_user.id)).scalar_one_or_none()
        
        if request.method == "GET":    
            comments = []
            thread = cached_data["id_mapping"].get(id)
            comments.append(serialize_comment(thread, bzaccs))
            
            for reply in thread["replies"]:
                comments.append(serialize_comment(reply, bzaccs))
                
            return jsonify(comments)       
        if request.method == "PUT":
            return jsonify(), 200
            # if isThreadByUser(int(id), current_user):
            #     if "unread" not in request.get_json():
            #         return jsonify({"error", "Read status not specified"}), 500
                
            #     thread = db.session.execute(db.select(IGThread).filter_by(id=int(id))).scalar_one_or_none()
            #     if thread is not None:
            #         status = request.get_json()["unread"]
            #         thread.is_unread = status
            #         db_handler.commitAllToDB([thread])
            #         #print(thread)
            #         return jsonify(), 200
            # else:
            #     return jsonify({"error":"ID not associated with user account"}), 500
        
        if request.method == "DELETE":
            return jsonify(), 200
            # if isThreadByUser(int(id), current_user):
            #     thread = db.session.execute(db.select(IGThread).filter(IGThread.id == int(id))).scalar_one_or_none()
            #     if thread is not None:
            #         # TL Kommentar zum Thread suchen
            #         tl_comment = next((c for c in thread.comments if c.parent is None), None)
            #         if tl_comment is not None:
            #             # FB Request für Kommentar löschen                        
            #             req = IGApiFetcher.deleteIGObject(current_user.oauth.token['access_token'], tl_comment.fb_id)
            #             if "success" in req.json() and req.json()["success"] == True:
            #                 db_handler.deleteFromDB(thread.comments)
            #                 db_handler.deleteFromDB([thread])
            #                 return jsonify(), 200
            #             else:
            #                 return jsonify({"error":f"Instagram error while deleting, {req.json()['error']['message']}"}), 500
            #         else:
            #             return jsonify({"error":"Top level comment for thread not found"}), 500
            #     else:
            #         return jsonify({"error":f"Thread with id {id} not found"}), 500
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occoured"}), 500

@threads_bp.route("/<id>/post", methods=["GET"])
@login_required
def get_post_information(id):
    try:
        caching_key = f"media_trees_{current_user.id}"
        cached_data = loadCachedResults.delay(current_user.oauth.token["access_token"], caching_key, current_user.id).get()
        
        fb_id = cached_data["id_mapping"].get(id)["media"]
        
        media = db.session.execute(db.select(IGMedia).filter(IGMedia.fb_id == fb_id)).scalar_one_or_none()
        if media is None:
            return jsonify({"error":"No media with given id found in DB"})
        
        return jsonify({
            "id": media.fb_id,
            "permalink": media.permalink,
            "mediaType": media.media_type,
            "postMedia": media.media_url,
            "postContent": media.caption,
            "platform": _PlatformEnum.Instagram.name,
            "likes": media.like_count,
            "comments": media.comments_count,
            "shares": None,
            "timestamp": media.timestamp
        }), 200
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occoured"}), 500

@threads_bp.route("/<id>/message", methods=["POST"])
@login_required
def post_message(id):
    try:
        body = request.get_json()
        if "message" not in body or body["message"] == "":
            return jsonify({"error": "No message specified"}), 400
        
            
        #print(current_user.organization)
        caching_key = f"media_trees_{current_user.id}"
        res = IGApiFetcher.postReplyToComment(current_user.oauth.token["access_token"], id, body['message'])
        cached_data = loadCachedResults.delay(current_user.oauth.token["access_token"], caching_key, current_user.id).get()
        
        # tabelle mit Verbesserungen erweitern
        if "generated_message" in body:
            
            fb_id = cached_data["id_mapping"].get(id)["media"]
            
            media = db.session.execute(db.select(IGMedia).filter(IGMedia.fb_id == fb_id)).scalar_one_or_none()
            loadCachedResults.delay(current_user.oauth.token["access_token"], caching_key, current_user.id, updated_media_id=media.fb_id)
            improvement = AnswerImprovements(generated_answer=body["generated_message"], improved_answer=body["message"], user=current_user, media=media)
            db.session.add(improvement)
            db.session.commit()
        return jsonify(), 200
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occoured"}), 500
    
# @threads_bp.route("/bookmarks", methods=["GET"])
# @login_required
# def get_bookmarked_threads():
#     try:
#         # pages für den user finden
#         pages = db.session.execute(db.select(IGPage).filter_by(user=current_user)).scalars().all()
#         media_ids = []
#         for p in pages:
#             for b in p.business_accounts:
#                 for m in b.medias:
#                     media_ids.append(m.id)
        
#         # alle Threads finden  
#         stmt = db.select(IGThread).filter(IGThread.media_id.in_(media_ids)).filter_by(is_bookmarked=True).limit(20)
#         if request.args.get("offset"):
#             try:
#                 stmt.offset((int(request.args.get("offset")) - 1) * 20)
#             except Exception:
#                 return jsonify({"error" : "Offset is not a number"}), 500
#         threads = db.session.execute(stmt).scalars().all()
#         # Response Objekt bauen, thread um Customer Daten und letzte aktuelle message des Threads + lastUpdated (= zeitpunkt der letzten aktuellen message)
#         results = []
#         for at in threads:
#             last_comment = sorted(at.comments, key=lambda x: x.timestamp)[-1]
#             results.append(thread_result_obj(at, last_comment))
            
#         return jsonify(results)
#     except Exception:
#         print(traceback.format_exc())
#         return jsonify({"error":"An exception has occoured"}), 500

# @threads_bp.route("/bookmarks/<threadId>", methods=["PUT"])
# @login_required
# def update_bookmarks(threadId):
#     try:
#         if request.method == "PUT":
#             pages = db.session.execute(db.select(IGPage).filter_by(user=current_user)).scalars().all()
#             media_ids = []
#             for p in pages:
#                 for b in p.business_accounts:
#                     for m in b.medias:
#                         media_ids.append(m.id)
            
#             # alle Threads finden            
#             thread = db.session.execute(db.select(IGThread)
#                                          .filter(IGThread.media_id.in_(media_ids))
#                                          .filter_by(id=int(threadId))).scalar_one_or_none()
#             if thread is None:
#                 return jsonify({"error":"Thread ID not associated with user"}), 500
            
#             if "bookmarked" not in request.get_json():
#                 return jsonify({"error", "Illegal bookmarked status"}), 500
            
#             thread.is_bookmarked = request.get_json()["bookmarked"]
#             db.session.add(thread)
#             db.session.commit()
#             return jsonify(), 200
#     except Exception:
#         print(traceback.format_exc())
#         return jsonify({"error":"An exception has occoured"}), 500
