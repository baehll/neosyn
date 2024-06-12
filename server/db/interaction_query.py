from .db_handler import *
from .models import *
from flask import current_app
from flask_login import current_user
from ..social_media_api.IGApiFetcher import _getETagsForExistingObjs
# STRUCTURE
    # comments list
    # medias list

def loadCachedResults(cache_id):
    comments, medias = [], []
    try:
        comments = current_app.cache.get(cache_id)["comments"]
        medias = current_app.cache.get(cache_id)["medias"]
    except:
        medias = db.session.execute(db.select(IGMedia).join(IGBusinessAccount).join(IGPage).join(User).filter(User.id == current_user.id)).scalars().all()
    findUpdatedMedias(current_user.oauth.token["access_token"], medias)
    
    return comments, medias

def findUpdatedMedias(access_token, db_objs):
    return _getETagsForExistingObjs(access_token, db_objs)

# sortCommentsByTimestamps(reverse=False)
 
# getLatestComments(access_token, offset) 
    # überprüfe Etags
        # wenn Etag anders, 
            # alle neusten kommentare (mit timestamp < latest_comment_timestamp) zu Beginn der Liste einfügen
            
    # 10 Kommentare je 10 Media betrachten
    # alle zu einer Liste vereinen
    # nach timestamp sortieren 
    # mit Offset die nächsten 20 Kommentare zurückgeben
        # wenn Offset + 20 > menge an Kommentaren
            # nächsten 10 Kommentare je 10 Media sammeln
            # zu liste vereinen
            # liste sortieren nach timestamp
    # return