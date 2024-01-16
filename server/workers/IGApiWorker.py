from ..web.models import db, Page, Business_Account, Media, Comment
import requests

_URL = "https://graph.facebook.com/v18.0"
# TASKS = ["ADVERTISE", "ANALYZE", "CREATE_CONTENT", "MESSAGING", "MODERATE", "MANAGE"]

# request gegen IG Graph API für die IDs (pre Batches)
def _getIDs(access_token, path):
    request_url = _URL + path + f"?access_token={access_token}"
    return requests.get(url=request_url)
    
# https://developers.facebook.com/docs/graph-api/batch-requests/
def _batchRequest(access_token, path, json_p, headers=""):
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
    
    # wenn es keine gibt, dann den Header nicht setzen
    if pages.count() == 0:
        # alle Pages des Users abfragen
        page_res = _getIDs(access_token, "/me/accounts")
        
        new_pages = []
        if page_res.status_code == 200:
            for p in page_res.json()["data"]:
                new_page = Page(name=p["name"], category=p["category"], fb_id=p["id"])
                
                # Tasks befüllen
                for pt in page["tasks"]:
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
            # wenn status == 200: neuen ETAG speichern und permissions updaten
    
    # DB commits, wenn es welche gibt
    
    page_ids = []
    res = requests.get(url=_URL+f"/me/accounts?access_token={access_token}")
    if res.status_code == 200:
        db.session.begin()
        try:
            data = res.json()["data"]    
            # für jede page in der antwort einen db eintrag erstellen
            for page in data:
                # neues Page objekt erstellen
                new_page = Page(name=page["name"], category=page["category"], etag=res.headers["ETag"], fb_id=page["id"])
                
                # Tasks befüllen
                for pt in page["tasks"]:
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
                        
                # mit UserToken verknüpfen
                usertoken.pages.append(new_page)
                page_ids.append(page["id"])
                
                db.session.add(new_page)
                
            db.session.add(usertoken)
            
            # commit
            db.session.commit()
        except:
            db.session.flush()
        
    # return der page_id's
    return page_ids

def getBusinessAccounts(access_token, page):
    bz_accs = []
    # alle IG User zur Page holen
    res = requests.get(url=_URL+f"/{page.fb_id}?fields=instagram_business_account,followers_count&access_token={access_token}")
    
    if res.status_code == 200:
        db.session.begin()
        try:
            data = res.json()["data"]
            
            # für jeden IG User einen Eintrag erstellen
            for acc in data:
                new_bz_acc = Business_Account(followers_count=acc["followers_count"], etag=res.headers["ETag"], fb_id=acc["id"])
                
                bz_accs.append(new_bz_acc)
                page.business_accounts.append(new_bz_acc)
                
                db.session.add(new_bz_acc)
            db.session.commit()
        except:
            db.session.flush()
            
    # return der business account ids
    return bz_accs

def getMedia(access_token, bz_acc):
    medias = []
    
    # zuerst alle IG Media IDs sammeln
    res = requests.get(url=_URL+f"/{bz_acc.fb_id}/media?access_token={access_token}")
    
    if res.status_code == 200:
        media_ids = res.json()["data"]
        for id in media_ids:
            # TODO Batch Request an Meta API
            media_res = requests.get(url=_URL+f"/{id}?access_token={access_token}&fields=media_url,timestamp,permalink")
            
            if media_res.status_code == 200:
                db.session.begin()
                try:    
                    media_data = media_res.json()["data"]
                    
                    for m in media_data:
                        new_media = Media(timestamp=m["timestamp"], permalink=m["permalink"], media_url=m["media_url"], 
                                        etag=media_res.headers["ETag"], fb_id=m["id"])
                        bz_acc.media.append(new_media)
                        medias.append(new_media)
                        db.session.add(new_media)
                    
                    db.session.commit()
                except:
                    db.session.flush()
    return medias

def getComments(access_token, media):
    comments = []
    res = requests.get(url=_URL+f"/{media.fb_id}/comments?fields=replies,id,timestamp&access_token={access_token}")
    
    if res.status_code == 200:
        db.session.begin()
        try:
            data = res.json()["data"]
            
            # für jeden IG User einen Eintrag erstellen
            for comm in data:
                new_comm = Comment(timestamp=comm["timestamp"], etag=res.headers["ETag"], fb_id=comm["id"])
                
                comments.append(new_bz_acc)
                media.business_accounts.append(new_bz_acc)
                
                db.session.add(new_bz_acc)
            db.session.commit()
        except:
            db.session.flush()
            
    # return der business account ids
    return comments
    