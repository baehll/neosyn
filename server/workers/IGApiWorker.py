from ..web.models import db, Page, BusinessAccount, Media, Comment
import requests, json
from datetime import datetime

_URL = "https://graph.facebook.com/v18.0"
# TASKS = ["ADVERTISE", "ANALYZE", "CREATE_CONTENT", "MESSAGING", "MODERATE", "MANAGE"]

# request gegen IG Graph API für die IDs (pre Batches)
def _getIDs(access_token, path, fields=""):
    request_url = _URL + path
    if fields != "":
        request_url += "?fields=" + fields + f"&access_token={access_token}"
    else:
        request_url += f"?access_token={access_token}"
    return requests.get(url=request_url)
    
# https://developers.facebook.com/docs/graph-api/batch-requests/
# batch requests gehen gegen irgendeinen path, da jede request eine eigene relative URL hat
def _batchRequest(access_token, payload):
    return requests.post(url=_URL+f"?access_token={access_token}", params={"batch": json.dumps(payload)})

# commit eine ganze Iterable in DB
def _commitToDB(data):
    try:
        db.session.add_all(data)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()

# Holt alle ETags für die db_objs, die noch nicht in der Datenbank sind
def _getETagsForNewObjs(access_token, db_objs):
    payload = []
    for o in db_objs:
        payload.append({"method" : "GET", "relative_url": f"{o.fb_id}"})
    resp = _batchRequest(access_token, payload)
    for res in resp.json():
        if res["code"] == 200:
            etag = [e for e in res["headers"] if e.get("name") == "ETag"].pop()["value"]
            obj_id = json.loads(res["body"])["id"]
            update_obj = next((obj for obj in db_objs if obj.fb_id == obj_id), None)
            if update_obj:
                update_obj.etag = etag
    return db_objs  

# 1. payload mit db daten bauen + relevanten feldern
# 2. antwort von meta nach 304 code filtern
# 3. alle db einträge mit neuen Meta API daten überschreiben
def _getETagsForExistingObjs(access_token, fields, db_objs):
    payload = []
    for o in db_objs:
        payload.append({"method" : "GET", "relative_url": f"{o.fb_id}?fields={fields}", "headers" : f'["If-None-Match: {o.etag}"]'})
    # Batch Requests für die mehrzahl an db_objs aus der DB
    res = _batchRequest(access_token, payload)
    
    updated_objs = []
    if res.status_code == 200:
        old_meta_objs = res.json()
        for acc in old_meta_objs: 
            # Wenn Status == 304, dann hat sich nichts geändert 
            if acc["code"] != 304:
                updated_objs.append(acc)

    return updated_objs

# Aktualisiert gegebene Einträge mit neuen Informationen aus den neuen Einträgen
def _updateExistingEntries(entries, changed_data):
    for entry in entries:
        for d in changed_data:
            body = json.load(d["body"])
            # den jeweiligen ETag Header aus der Liste der Header extrahieren
            etag_header = [e for e in d["headers"] if e.get("name") == "ETag"].pop()
            if entry.fb_id == body["id"]:
                entry.etag = etag_header
                for key,value in changed_data.items():
                    setattr(entry, key, value)
        
# request mit dem jeweiligen ETag der Pages falls vorhanden. erstellt und updatet Pages für gegebenen Usertoken
def getPages(access_token, usertoken):
    _fields = "name,category,id,followers_count,tasks"
    # in DB nach pages für den usertoken gucken
    pages = db.session.execute(db.select(Page).filter_by(usertokens=usertoken)).scalars().all()
    new_pages = []
    
    # wenn es keine gibt, dann den Header nicht setzen
    if len(pages) == 0:
        # alle Pages des Users abfragen
        page_res = _getIDs(access_token, "/me/accounts", _fields)
        
        if page_res.status_code == 200:
            
            for p in page_res.json()["data"]:
                new_page = Page(name=p["name"], category=p["category"], fb_id=p["id"], followers_count=p["followers_count"])
                
                # Tasks befüllen
                for pt in p["tasks"]:
                    if pt == "ADVERTISE":
                        new_page.can_advertise = True
                    elif pt == "ANALYZE":
                        new_page.can_analyze = True
                    elif pt == "CREATE_CONTENT":
                        new_page.can_create_content = True
                    elif pt == "MESSAGING":
                        new_page.can_message = True
                    elif pt == "MODERATE":
                        new_page.can_moderate = True
                    elif pt == "MANAGE":
                        new_page.can_manage = True
                
                usertoken.pages.append(new_page)
                new_pages.append(new_page)
                
            _getETagsForNewObjs(access_token, new_pages)
            _commitToDB(new_pages + [usertoken])
        else:
            #TODO error handling
            print("Error while fetching data from Meta")
            print(page_res.json())
    else:        
        updated_pages = _getETagsForExistingObjs(access_token, _fields, pages)

        # zu Updatene Einträge finden und aktualisieren
        entries = db.session.execute(db.select(Page).filter(Page.fb_id.in_(updated_pages))).scalars().all()
        _updateExistingEntries(entries, updated_pages)
        
        _commitToDB(entries) 
        return entries 
    # return der page_id's
    return new_pages

def getBusinessAccounts(access_token, page):
    _fields = r"instagram_business_account{followers_count},followers_count"
    bz_accs = db.session.execute(db.select(BusinessAccount).filter(BusinessAccount.page.has(id=page.id))).scalars().all()
    new_bz_accs = []
    
    if len(bz_accs) == 0:
        # alle IG User zur Page holen
        bs_res = _getIDs(access_token, f"/{page.fb_id}", fields=_fields)
        if bs_res.status_code == 200:
            #page.etag = bs_res.headers["ETag"]
            page.followers_count = bs_res.json()["followers_count"]
            
            # aus der Antwort neue BZ_Accs erstellen
            bz = bs_res.json()["instagram_business_account"]
            new_bz_acc = BusinessAccount(fb_id=bz["id"], followers_count=bz["followers_count"])
            page.business_accounts.append(new_bz_acc)
            new_bz_accs.append(new_bz_acc)
            
            _getETagsForNewObjs(access_token, new_bz_accs)
            _commitToDB(new_bz_accs + [page])
        else:
            print(bs_res.json())
    else:
        updated_accs = _getETagsForExistingObjs(access_token, _fields, bz_accs)

        # zu Updatene Einträge finden und aktualisieren
        entries = db.session.execute(db.select(BusinessAccount).filter(BusinessAccount.fb_id.in_(updated_accs))).scalars().all()
        _updateExistingEntries(entries, updated_accs)
        
        _commitToDB(entries) 
        return entries
    # return der business account ids
    return new_bz_accs

def getMedia(access_token, bz_acc):
    _fields = "media_url,timestamp,permalink"
    medias = db.session.execute(db.select(Media).filter(Media.bzacc.has(id=bz_acc.id))).scalars().all()
    new_medias = []
    
    if len(medias) == 0:
        # zuerst alle IG Media IDs sammeln
        res = _getIDs(access_token, f"/{bz_acc.fb_id}/media")
        
        if res.status_code == 200:
            media_ids = res.json()["data"]
            
            # Batch Request an Meta API mit allen Media_IDs
            payload = []
            for media in media_ids:
                payload.append({"method" : "GET", "relative_url": f"{media['id']}?fields="+_fields})
            res = _batchRequest(access_token, payload)
                
            if res.status_code == 200:
                for m in res.json():
                    if m["code"] == 200:
                        body = json.loads(m["body"])
                        new_media = Media(timestamp=datetime.strptime(body["timestamp"], "%Y-%m-%dT%H:%M:%S%z"), permalink=body["permalink"], media_url=body["media_url"], fb_id=body["id"])
                        new_medias.append(new_media)
                        bz_acc.medias.append(new_media)
                    else:
                        print(m)
                _getETagsForNewObjs(access_token, new_medias)
                _commitToDB(new_medias + [bz_acc])
            else:
                pass
    else:
        updated_media = _getETagsForExistingObjs(access_token, _fields, medias)

        # zu Updatene Einträge finden und aktualisieren
        entries = db.session.execute(db.select(Media).filter(Media.fb_id.in_(updated_media))).scalars().all()
        _updateExistingEntries(entries, updated_media)
        
        _commitToDB(entries) 
        return entries
    return new_medias
    
def getComments(access_token, media):
    _fields = "replies{from, parent, timestamp, username},id,timestamp,from"
    comments = db.session.execute(db.select(Comment).filter(Comment.media.has(id=media.id))).scalars().all()
    new_comments = []

    if len(comments) == 0:
        res = _getIDs(access_token, f"/{media.fb_id}/comments")
        if res.status_code == 200:
            comment_ids = res.json()["data"]

            # Batch Request, um an alle ETags zu kommen
            payload = []
            for com in comment_ids:
                payload.append({"method": "GET", "relative_url": f"{com['id']}?fields="+_fields})

            batchRes = _batchRequest(access_token, payload)
            if batchRes.status_code == 200:
                for c in batchRes.json():
                    if c["code"] == 200:
                        body = json.loads(c["body"])
                        new_comm = Comment(timestamp=datetime.strptime(body["timestamp"], "%Y-%m-%dT%H:%M:%S%z"), fb_id=body["id"], from_user=body["from"]["id"])
                        new_comments.append(new_comm)
                        media.comments.append(new_comm)
                        print(body)
                        if "replies" in body:
                            for r in body["replies"]["data"]:
                                reply = Comment(timestamp=datetime.strptime(body["timestamp"], "%Y-%m-%dT%H:%M:%S%z"), fb_id=r["id"], from_user=r["from"]["id"])
                                new_comm.children.append(reply)
                                new_comments.append(reply)
                                media.comments.append(reply)
                    else:
                        print(c)
                _getETagsForNewObjs(access_token, new_comments)
                _commitToDB(new_comments + [media])
    else:        
        updated_comments = _getETagsForExistingObjs(access_token, _fields, comments)

        # zu Updatene Einträge finden und aktualisieren
        entries = db.session.execute(db.select(Comment).filter(Comment.fb_id.in_(updated_comments))).scalars().all()
        _updateExistingEntries(entries, updated_comments)
        
        _commitToDB(entries) 
        return entries
    # return der business account ids
    return new_comments
    
def getReplies(access_token, com):
    
    # erst prüfen, ob dieses kommentar überhaupt replies auf insta hat, danach normal weiter
    replies = db.session.execute(db.select(Comment).filter_by(fb_id=com.fb_id)).scalars.all()
    new_replies = []

    if replies.count() == 0:
        res = _getIDs(access_token, )
    else:
        pass