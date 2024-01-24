from ..web.models import db, Page, BusinessAccount, Media, Comment
import requests, json

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

# Baut aus einer Liste von Datenbank objekten den Payload für einen Batchrequest
def _payloadBuilder(data):
    pass

# commit eine ganze Iterable in DB
def _commitToDB(data):
    db.session.begin()
    try:
        db.session.add_all(data)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.flush()
        
# request mit dem jeweiligen ETag der Pages falls vorhanden. erstellt und updatet Pages für gegebenen Usertoken
def getPages(access_token, usertoken):
    # in DB nach pages für den usertoken gucken
    pages = db.session.execute(db.select(Page).filter_by(usertoken=usertoken)).scalars().all()
    new_pages = []
    
    # wenn es keine gibt, dann den Header nicht setzen
    if pages.count() == 0:
        # alle Pages des Users abfragen
        page_res = _getIDs(access_token, "/me/accounts", "tasks,starring,id,category,category_list")
        
        if page_res.status_code == 200:
            for p in page_res.json()["data"]:
                new_page = Page(name=p["name"], category=p["category"], fb_id=p["id"])
                
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
        # new_pages erstellen (=> Initialisierung)
        _commitToDB(new_pages + [usertoken])
    else:
        # ETags für /me/accounts sind nicht beständig und ändern sich, deshalb müssen die ETags der Pages einzeln gezogen werden 
        pass
        # für jeden Eintrag:
            # wenn status == 304: skip
    
    # return der page_id's
    return new_pages

def getBusinessAccounts(access_token, page):
    bz_accs = db.session.execute(db.select(BusinessAccount).filter_by(page=page)).scalars().all()
    new_bz_accs = []
    
    if bz_accs.count() == 0:
        # alle IG User zur Page holen
        bs_res = _getIDs(access_token, f"/{page.fb_id}", fields="instagram_business_account{{followers_count}},followers_count")
        if bs_res.status_code == 200:
            page.etag = bs_res.headers["ETag"]
            page.followers_count = bs_res.json()["followers_count"]
            
            # aus der Antwort neue BZ_Accs erstellen
            for bz in bs_res.json()["instagram_business_account"]:
                new_bz_acc = BusinessAccount(fb_id=bz["id"], followers_count=bz["followers_count"])
                page.business_accounts.append(new_bz_acc)
                new_bz_accs.append(new_bz_acc)
            _commitToDB(new_bz_accs + [page])
    else:
        # Es existieren bereits business accounts, deshalb wird nur geprüft, ob sich etwas geändert hat über ETags
        payload = []
        for acc in bz_accs:
            if acc.etag != "":
                payload.append({"method" : "GET", "relative_url": f"{acc.fb_id}?fields=followers_count", "headers" : f'["If-None-Match: {acc.etag}"]'})
            else:
                payload.append({"method" : "GET", "relative_url": f"{acc.fb_id}?fields=followers_count"})
        
        updated_accs = []
        # Batch Requests für die mehrzahl an bz_accs aus der DB
        res = _batchRequest(access_token, payload)
        if res.status_code == 200:
            old_bz_accs = res.json()
            for acc in old_bz_accs: 
                # Wenn Status == 304, dann hat sich nichts geändert oder es gibt einen BZ_ACC, aber er hat keinen ETag
                if acc["code"] != 304:
                    updated_accs.append(acc)

        # zu Updatene Einträge finden und aktualisieren
        entries = BusinessAccount.query.filter(BusinessAccount.fb_id.in_([updated_acc["id"] for updated_acc in updated_accs])).all()
        for entry in entries:
            for acc in updated_accs:
                body = json.load(acc["body"])
                # den jeweiligen ETag Header aus der Liste der Header extrahieren
                etag_header = [e for e in acc["headers"] if e.get("name") == "ETag"].pop()
                if entry.fb_id == body["id"]:
                    entry.etag = etag_header
                    entry.followers_count = body["followers_count"]
    # return der business account ids
    return new_bz_accs

def getMedia(access_token, bz_acc):
    medias = db.session.execute(db.select(Media).filter_by(bzacc=bz_acc)).scalars().all()
    new_medias = []
    
    if medias.count() == 0:
        # zuerst alle IG Media IDs sammeln
        res = _getIDs(access_token, f"/{bz_acc.fb_id}/media")
        
        if res.status_code == 200:
            media_ids = res.json()["data"]
            
            # Batch Request an Meta API mit allen Media_IDs
            payload = []
            for id in media_ids:
                payload.append({"method" : "GET", "relative_url": f"{id}?fields=media_url,timestamp,permalink"})
            res = _batchRequest(access_token, payload)
                
            if res.status_code == 200:
                for m in res.json():
                    if m.status_code == 200:
                        body = json.loads(res["body"])
                        etag_header = [e for e in m["headers"] if e.get("name") == "ETag"].pop()
                        new_media = Media(timestamp=body["timestamp"], permalink=body["permalink"], media_url=body["media_url"], 
                                        etag=etag_header, fb_id=m["id"])
                        new_medias.append(new_media)
                        bz_acc.media.append(new_media)
                _commitToDB(new_medias + [bz_acc])
    else:
        # es gibt bereits Medias, deshalb müssen neue hinzugefügt werden und alte geupdatet werden
        pass
    return new_medias
    
def getComments(access_token, media):
    comments = db.session.execute(db.select(Comment).filter_by(media=media)).scalars().all()
    new_comments = []

    if comments.count() == 0:
        res = _getIDs(access_token, f"/{media.fb_id}/comments")
        if res.status_code == 200:
            comment_ids = res.json()["data"]

            # Batch Request, um an alle ETags zu kommen
            payload = []
            for id in comment_ids:
                payload.append({"method": "GET", "relative_url": f"{id}?fields=replies,id,timestamp"})

            batchRes = _batchRequest(access_token, payload)

            if batchRes.status_code == 200:
                for c in batchRes.json():
                    if c.status_code == 200:
                        body = json.loads(res["body"])
                        etag_header = [e for e in c["headers"] if e.get("name") == "ETag"].pop()
                        new_comm = Comment(timestamp=body["timestamp"], etag=etag_header, fb_id=body["id"])
                        new_comments.append(new_comm)
                        media.comments.append(new_comm)
                _commitToDB(new_comments + [media])
    else:
        pass

    # return der business account ids
    return comments
    
def getReplies(access_token, com):
    # erst prüfen, ob dieses kommentar überhaupt replies auf insta hat
    replies = db.session.execute(db.select(Comment).filter_by(fb_id=com.fb_id)).scalars.all()
    new_replies = []

    if replies.count() == 0:
        res = _getIDs(access_token, )
    else:
        pass