from dateutil import parser as date_parser
from ..web.models import db, IGPage, IGBusinessAccount, IGMedia, IGComment, IGCustomer, IGThread
import requests, json, traceback
from datetime import datetime

# UTILITY FUNCTIONS UND VARIABLEN

_URL = "https://graph.facebook.com/v19.0"
# TASKS = ["ADVERTISE", "ANALYZE", "CREATE_CONTENT", "MESSAGING", "MODERATE", "MANAGE"]
_UPDATE_OFFSET = 20
# request gegen IG Graph API für die IDs (pre Batches)
def _getIDs(access_token, path, fields="", url=""):
    request_url = _URL + path
    if fields != "":
        request_url += "?fields=" + fields + f"&access_token={access_token}"
    else:
        request_url += f"?access_token={access_token}"
    
    req = requests.get(url=request_url)
    # print(req.json())
    # print("######")
    if req.status_code == 200:
        return req
    else:
        print("ID Request GET returned " + str(req.status_code) + f", (URL: {path}, Fields: {fields} )")
 
# Liefert eine Liste an allen Einträgen, die unter dem Path und den Fields vorhanden sind, inkl. paging results (wenn in einer Response > 25 Einträge sind)
def _getInstagramData(access_token, path, fields=""):
    ids = _getIDs(access_token, path, fields)
    results = []
    if "data" in ids.json():
        results = ids.json()["data"]
        # Paging Results, wenn vorhanden, werden iterativ abgefragt und an results angehängt
        #print(ids.json()["paging"]["next"])
        while "paging" in ids.json() and "next" in ids.json()["paging"]:
            req_url = ids.json()["paging"]["next"]
            req = requests.get(url=req_url)
            if req.status_code == 200:
                results.extend(req.json()["data"])
                ids = req
            else:
                print("Paging Results GET returned " + str(req.status_code) + f", (URL: {req_url})")
    else:
        results.append(ids.json())
    #print(results)
    return results
            

# https://developers.facebook.com/docs/graph-api/batch-requests/
# batch requests gehen gegen irgendeinen path, da jede request eine eigene relative URL hat
# da nur der ETag Header und Body interessant sind, wird der Rest ausgefiltert
# Wenn es in einem Result Paging Ergebnisse gibt, werden die ebenfalls angehangen
def _batchRequest(access_token, payload):
    results = []
    position = 0
    while True:
        # Max Batch Size für Meta ist 50, deshalb werden in 50er Schritten Batchabfragen geschickt
        # wenn das Ende der Slice über die Länge des Arrays hinausgeht, wird einfach der ganze Rest iteriert
        # inkl. Start exkl. Ende
        req = requests.post(url=_URL+f"?access_token={access_token}", params={"batch": json.dumps(payload[position:(position+50)])})
        
        if req.status_code == 200:
            for entry in req.json():
                # jede Batchantwort hat einen eigenen Statuscode
                if entry["code"] == 200:
                    #etag = [e for e in entry["headers"] if e.get("name") == "ETag"].pop()["value"]
                    body = json.loads(entry["body"])
                    
                    # IDs aus dem Paging Ergebnis zum Payload hinzufügen, wenn es welche gibt
                    paging_results = _resolvePaging(body)
                    if(len(paging_results) > 0):
                        payload.extend(paging_results)
                    
                    results.append(body)
                elif entry["code"] == 304:
                    # Ein ETag Header war gesetzt und nichts hat sich verändert
                    continue
                else:
                    print("Single Batchrequest Entry returned " + str(entry["code"]) + ", Message: " + entry["body"])
        elif req.status_code == 304:
            print("Batch Request POST returned 304, skipping")
        else:
            print("Batch Request POST returned " + str(req.status_code) + f", (JSON: {req.json()})")
        
        # Wenn das verschieben um 50 Stellen außerhalb des Arrays läge, sind wir fertig, ansonsten an der neuen Stelle weitermachen
        if position+50 > len(payload):
            break
        else:
            position += 50 
    return results

# Alle Paging Links zu diesem Knoten werden aufgelöst, liefert Objekte für Batch requesting
def _resolvePaging(node):
    results = []
    
    url = ""
    if "paging" in node:
        url = node["paging"]["next"]
    if "data" in node and "paging" in node["data"]:
        url = node["data"]["paging"]["next"]
    # Special Case für Replies von comments
    elif "replies" in node and "paging" in node["replies"]:
        url = node["replies"]["paging"]["next"] 
    else:
        return results
    
    if url != "":
        req = requests.get(url=url)
        if req.status_code == 200:
            #print(req.json())
            results.extend([{"method" : "GET", "relative_url": f"{n['id']}"} for n in req.json()["data"]])
        
    return results

# commit eine ganze Iterable in DB
def _commitToDB(data):
    try:
        db.session.add_all(data)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()

def _deleteFromDB(data):
    try:
        for d in data:
            db.session.delete(d)
        db.session.commit()
    except Exception:
        print(traceback.format_exc())
        db.session.rollback()

# Holt alle ETags für die db_objs, die noch nicht in der Datenbank sind
def _getETagsForNewObjs(access_token, db_objs):
    payload = []
    for o in db_objs:
        payload.append({"method" : "GET", "relative_url": f"{o.fb_id}"})
    results = _batchRequest(access_token, payload)
    
    for res in results:
        #print(res)
        obj_id = res["body"]["id"]
        update_obj = next((obj for obj in db_objs if obj.fb_id == obj_id), None)
        if update_obj:
            update_obj.etag = res["etag"]
                
    return db_objs  

# Liefert alle veränderten FB-Objekte basierend auf existierenden Objekten und ihren ETags
def _getETagsForExistingObjs(access_token, fields, db_objs):
    updated_objs = []
    payload = []    
    for o in db_objs:
        #payload.append({"method" : "GET", "relative_url": f"{o.fb_id}?fields={fields}", "headers" : [f'If-None-Match: {o.etag}']})
        if hasattr(o, "etag"):
            payload.append({"method" : "GET", "relative_url": f"{o.fb_id}", "headers": [f'If-None-Match: {o.etag}']})
        else:
            payload.append({"method" : "GET", "relative_url": f"{o}"})
    # Batch Requests für die mehrzahl an db_objs aus der DB
    res = _batchRequest(access_token, payload)

    for acc in res: 
        # Extra Logik für Replies, um das Array abzuflachen
        if "replies" in acc["body"]:
            for r in acc["body"]["replies"]["data"]:
                updated_objs.append(r)
        else:
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
        
# FUNCTIONS

# request mit dem jeweiligen ETag der Pages falls vorhanden. erstellt und updatet Pages für gegebenen Usertoken
def getPages(access_token, user):
    _fields = "name,category,id,followers_count" # + ",tasks"
    
    pages = db.session.execute(db.select(IGPage).filter(IGPage.user.has(id=user.id))).scalars().all()
    #pages = db.session.execute(db.select(Page).filter(Page.user.has(id=user.id))).scalar_one_or_none()
    new_pages = []
    # alle Pages des Users abfragen
    page_res = _getInstagramData(access_token, "/me/accounts", _fields)
    
    # Batch Request an Meta API mit allen Page_IDs
    payload = []
    for p in page_res:
        #print(multi_pages)
        payload.append({"method" : "GET", "relative_url": f"{p['id']}?fields="+_fields})
    page_res = _batchRequest(access_token, payload)
    
    if len(pages) > 0:
        # bereits vorhandene Einträge nicht einfügen
        existing_pages_fb_ids = [p.fb_id for p in pages]
        page_res_filtered = page_res.copy()
        
        for all_pages in page_res_filtered:
            p = all_pages
            if p["id"] in existing_pages_fb_ids:
                page_res.remove(all_pages)
    
    for p in page_res:
        new_page = IGPage(name=p["name"], category=p["category"], fb_id=p["id"], followers_count=p["followers_count"])
        # # Tasks befüllen
        # for pt in p["tasks"]:
        #     if pt == "ADVERTISE":
        #         new_page.can_advertise = True
        #     elif pt == "ANALYZE":
        #         new_page.can_analyze = True
        #     elif pt == "CREATE_CONTENT":
        #         new_page.can_create_content = True
        #     elif pt == "MESSAGING":
        #         new_page.can_message = True
        #     elif pt == "MODERATE":
        #         new_page.can_moderate = True
        #     elif pt == "MANAGE":
        #         new_page.can_manage = True
        
        user.pages.append(new_page)
        new_pages.append(new_page)
    
    _commitToDB(new_pages + [user])    
    
    # return der page_id's
    return new_pages

def getBusinessAccounts(access_token, page):
    _fields = r"instagram_business_account{followers_count},followers_count"
    bz_accs = db.session.execute(db.select(IGBusinessAccount).filter(IGBusinessAccount.page.has(id=page.id))).scalars().all()
    new_bz_accs = []
    
    bs_res = _getInstagramData(access_token, f"/{page.fb_id}", fields=_fields)
    
    if len(bz_accs):
        # bereits vorhandene Einträge nicht einfügen
        existing_bz_accs_fb_ids = [b.fb_id for b in bz_accs]
        bs_res_filtered = bs_res.copy()
        
        for b in bs_res_filtered:
            if b["instagram_business_account"]["id"] in existing_bz_accs_fb_ids:
                bs_res.remove(b)
            
    # aus der Antwort neue BZ_Accs erstellen
    for bz in bs_res:
        new_bz_acc = IGBusinessAccount(fb_id=bz["instagram_business_account"]["id"], followers_count=bz["instagram_business_account"]["followers_count"])
        page.business_accounts.append(new_bz_acc)
        page.followers_count = bz["followers_count"]
        new_bz_accs.append(new_bz_acc)
    
    _commitToDB(new_bz_accs + [page])

    return new_bz_accs

def getMedia(access_token, bz_acc):
    _fields = "media_url,timestamp,permalink,comments_count,like_count,caption,media_type"
    medias = db.session.execute(db.select(IGMedia).filter(IGMedia.bzacc.has(id=bz_acc.id))).scalars().all()
    new_medias = []
    
    # zuerst alle IG Media IDs sammeln
    res = _getInstagramData(access_token, f"/{bz_acc.fb_id}/media")
    # Batch Request an Meta API mit allen Media_IDs
    payload = []
    for m in res:
        payload.append({"method" : "GET", "relative_url": f"{m['id']}?fields="+_fields})
    media_res = _batchRequest(access_token, payload)
    
    if len(medias) > 0:
        # bereits vorhandene Einträge nicht einfügen
        existing_medias_fb_ids = [m.fb_id for m in medias]
        media_res_filtered = media_res.copy()
        for m in media_res_filtered:
            if m["id"] in existing_medias_fb_ids:
                media_res.remove(m)
    
    for body in media_res:
        new_media = IGMedia(timestamp=date_parser.isoparse(body["timestamp"]), 
                            permalink=body["permalink"], 
                            media_url=body["media_url"], 
                            fb_id=body["id"],
                            like_count=body["like_count"],
                            comments_count=body["comments_count"],
                            caption=body["caption"],
                            media_type=body["media_type"])
        
        new_medias.append(new_media)
        bz_acc.medias.append(new_media)
    _commitToDB(new_medias + [bz_acc])

    return new_medias
    
def getComments(access_token, media):
    _fields = "replies{from, parent, timestamp, username,text,like_count},id,timestamp,from,text,like_count"
    db_comments = db.session.execute(db.select(IGComment).filter(IGComment.media.has(id=media.id))).scalars().all()

    res = _getInstagramData(access_token, f"/{media.fb_id}/comments")
    
    payload = []
    
    for com in res:
        payload.append({"method": "GET", "relative_url": f"{com['id']}?fields=" + _fields})
    com_res = _batchRequest(access_token, payload)
    
    deletable_comment_ids, new_comment_ids, updateable_comment_ids, comment_customer, new_comments = [], [], [], [], []

    db_comment_dict = dict([(c.fb_id, c) for c in db_comments])
    fb_comment_dict = dict()
    for c in com_res:
        fb_comment_dict[c["id"]] = c
        if "replies" in c:
            for r in c["replies"]["data"]:
                fb_comment_dict[r["id"]] = r
    '''	
    Welche Kommentare sind in fb_comments, aber nicht in db_comments -> hinzufügen
    Welche Kommentare sind in db_comments, aber nicht in fb_comments -> delete
    Schnittmenge fb_comments db_comments -> update
    '''
    # Sets zur Anwendung von Mengenoperatoren
    db_comments_fb_ids = set(db_comment_dict.keys())
    fb_comment_ids = set(fb_comment_dict.keys()) 
    
    if len(db_comments) > 0:
        deletable_comment_ids = db_comments_fb_ids - fb_comment_ids
        updateable_comment_ids = db_comments_fb_ids & fb_comment_ids
    
    new_comment_ids = fb_comment_ids - db_comments_fb_ids
    
    print("creating comments " + str(len(new_comment_ids)))
    for id in new_comment_ids:
        body = fb_comment_dict[id]
        print(body)
        new_comm = IGComment(timestamp=date_parser.isoparse(body["timestamp"]), fb_id=body["id"], text=body["text"], like_count=body["like_count"])
        
        # User mit Media und Comment verknüpfen
        comment_customer.append((new_comm, body["from"]))
        new_comments.append(new_comm)
        if "replies" in body:
            for r in body["replies"]["data"]:
                reply = IGComment(timestamp=date_parser.isoparse(r["timestamp"]), fb_id=r["id"], text=r["text"], like_count=r["like_count"])
                comment_customer.append((reply, r["from"]))
                reply.parent = new_comm
                new_comments.append(reply)
                
    for comment, fb_user in comment_customer:
        # prüfen, ob customer in DB vorhanden ist, sonst hinzufügen und verbindung media - comment - customer erstellen
        db_customer = db.session.execute(db.select(IGCustomer).filter_by(fb_id=fb_user["id"])).scalar_one_or_none()

        # Wenn kein Customer bis jetzt existiert, neuen erstellen
        if db_customer is None:
            db_customer = IGCustomer(fb_id=fb_user["id"], name=fb_user["username"])
            _commitToDB([db_customer])            
        
        thread = db.session.execute(db.select(IGThread).filter_by(media=media).filter_by(customer=db_customer)).scalar_one_or_none()
        # Wenn es noch keinen Thread gibt, neuen erstellen
        if thread is None:
            thread = IGThread(media=media, customer=db_customer)
            _commitToDB([thread])
            
        comment.thread = thread
        comment.media = media
        comment.customer = db_customer
        
        _commitToDB([comment, media, db_customer, thread])
        thread.comments.append(comment)
        media.comments.append(comment)
        db_customer.comments.append(comment)
    
    if len(deletable_comment_ids) > 0:
        print("deleting comments " + str(len(deletable_comment_ids)))
        print(deletable_comment_ids)
        db_deletable_comments = [c for c in db_comments if c.fb_id in deletable_comment_ids]
        _deleteFromDB(db_deletable_comments)
    
    if len(updateable_comment_ids) > 0:
        print("updating comments " + str(len(updateable_comment_ids)))
        db_updateable_comments = [c for c in db_comments if c.fb_id in updateable_comment_ids]
        for com in db_updateable_comments:
            #print(fb_comment_dict[com.fb_id])
            fb_com_body = fb_comment_dict[com.fb_id]
            if fb_com_body is not None:
                com.text = fb_com_body["text"]
                com.timestamp = date_parser.isoparse(fb_com_body["timestamp"])
                com.like_count = fb_com_body["like_count"]
        
    _commitToDB([media])
    getCustomers(access_token, media)
    
    return new_comments
 
def getCustomers(access_token, media):
    _fields = "profile_picture_url"
        
    if len(media.customers) == 0:
        return
    
    payload = []
    for customer in media.customers:
        payload.append({"method": "GET", "relative_url": f"{customer.fb_id}?fields=" + _fields})
    customer_res = _batchRequest(access_token, payload)

    for body in customer_res:
        for c in media.customers:
            if c.fb_id == body["id"]:
                c.profile_picture_url = body["profile_picture_url"]
    
    _commitToDB([media])
    return
    
def updateInteractions(access_token, media_ids, interaction_id):
    # doppelter _UPDATE_OFFSET, um die eine hälfte jetzt zu updaten und die andere im Hintergrund zu updaten
    interactions = db.session.execute(db.select(IGThread).filter(IGThread.media_id.in_(media_ids)).offset(interaction_id).limit(_UPDATE_OFFSET*2)).scalars().all()
    print(interactions)
    # ab der ersten Interaction die nächsten _UPDATE_OFFSET updaten
    
    # ab der ersten Interaction + _UPDATE_OFFSET die nächsten _UPDATE_OFFSET updaten im Hintergrund 
    

def updateAllEntries(access_token, user):
    pages, bz_accs, medias, comments = [], [], [], []
    
    pages = getPages(access_token, user)
    if len(pages) == 0:
        pages = db.session.execute(db.select(IGPage).filter(IGPage.user.has(id=user.id))).scalars().all()
    for p in pages:
        bz_accs.extend(getBusinessAccounts(access_token, p))
    
    print("pages done")
    
    if len(bz_accs) == 0:
        for p in pages:
            bz_accs = db.session.execute(db.select(IGBusinessAccount).filter(IGBusinessAccount.page.has(id=p.id))).scalars().all()
    for b in bz_accs:
        medias.extend(getMedia(access_token, b))
        
    print("bzacc done")
    
    if len(medias) == 0:
        for b in bz_accs:
            medias = db.session.execute(db.select(IGMedia).filter(IGMedia.bzacc.has(id=b.id))).scalars().all()
    for m in medias:
        getComments(access_token, m)
