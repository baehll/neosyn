from dateutil import parser as date_parser
from ..db.models import db, IGPage, IGBusinessAccount, IGMedia
import requests, json
from ..db.db_handler import commitAllToDB, deleteFromDB
from urllib.parse import quote
# UTILITY FUNCTIONS UND VARIABLEN

_URL = "https://graph.facebook.com/v19.0"
# TASKS = ["ADVERTISE", "ANALYZE", "CREATE_CONTENT", "MESSAGING", "MODERATE", "MANAGE"]
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
 
# Liefert eine Liste an allen Einträgen, die unter dem Path und den Fields vorhanden sind, 
# inkl. paging results (wenn in einer Response > 25 Einträge sind)
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
                    etag = [e for e in entry["headers"] if e.get("name") == "ETag"].pop()["value"]
                    body = json.loads(entry["body"])
                    
                    # IDs aus dem Paging Ergebnis zum Payload hinzufügen, wenn es welche gibt
                    paging_results = _resolvePaging(body)
                    if(len(paging_results) > 0):
                        payload.extend(paging_results)
                    
                    results.append((body, etag))
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
def _getETagsForExistingObjs(access_token, db_objs, fields=""):
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

def _findIDDifferences(db_dict, fb_dict, db_data_exists):    
    '''	
    Welche Kommentare sind in fb_comments, aber nicht in db_comments -> hinzufügen
    Welche Kommentare sind in db_comments, aber nicht in fb_comments -> delete
    Schnittmenge fb_comments db_comments -> update
    '''
    db_fb_ids = set(db_dict.keys())
    fb_ids = set(fb_dict.keys())
    
    deleteable_ids, updateable_ids, new_page_ids = [], [], []
    
    if (db_data_exists):
        deleteable_ids = db_fb_ids - fb_ids
        updateable_ids = db_fb_ids & fb_ids
    
    new_page_ids = fb_ids - db_fb_ids
    
    return deleteable_ids, updateable_ids, new_page_ids

def _findMediasWithNewEtag(db_dict, fb_dict):
    db_fb_ids = set(db_dict.keys())
    fb_ids = set(fb_dict.keys())
    updateable_ids = db_fb_ids & fb_ids
    return [id for id in updateable_ids if fb_dict[id][1] != db_dict[id].etag]
       
# FUNCTIONS
def deleteIGObject(access_token, fb_id):
    return requests.delete(f"{_URL}/{int(fb_id)}?access_token={access_token}")

def postReplyToComment(access_token, tl_comment_id, reply_message):
    return requests.post(_URL + f"/{tl_comment_id}/replies?message={quote(reply_message)}&access_token={access_token}")

# request mit dem jeweiligen ETag der Pages falls vorhanden. erstellt und updatet Pages für gegebenen Usertoken
def getPages(access_token, user):
    _fields = "name,category,id,followers_count" # + ",tasks"
    db_pages = db.session.execute(db.select(IGPage).filter(IGPage.user.has(id=user.id))).scalars().all()
    
    new_pages = []
    # alle Pages des Users abfragen
    page_res = _getInstagramData(access_token, "/me/accounts", _fields)
    
    # Batch Request an Meta API mit allen Page_IDs
    payload = []
    for p in page_res:
        payload.append({"method" : "GET", "relative_url": f"{p['id']}?fields="+_fields})
    page_res = _batchRequest(access_token, payload)
    db_page_dict = dict([(pg.fb_id, pg) for pg in db_pages])
    fb_page_dict = dict([(pg["id"], (pg,etag)) for pg,etag in page_res])
    
    deletable_page_ids, updateable_page_ids, new_page_ids = _findIDDifferences(db_page_dict, fb_page_dict, len(db_pages) > 0)

    for id in new_page_ids:
        p = fb_page_dict[id][0]
        new_page = IGPage(name=p["name"], category=p["category"], fb_id=p["id"], followers_count=p["followers_count"], etag=fb_page_dict[id][1])
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
    
    commitAllToDB(new_pages + [user])    
    
    if len(deletable_page_ids) > 0:
        db_deletable_bzaccs = [b for b in db_pages if b.fb_id in deletable_page_ids]
        deleteFromDB(db_deletable_bzaccs)
        
    updated_pages = []
    if len(updateable_page_ids) > 0:
        db_updateable_pages = [m for m in db_pages if m.fb_id in updateable_page_ids]
        for page in db_updateable_pages:
            etag = fb_page_dict[page.fb_id][1]
            fb_page_body = fb_page_dict[page.fb_id][0]
            if fb_page_body is not None:
                page.etag = etag
                page.followers_count = fb_page_body["followers_count"]
                page.name = fb_page_body["name"]
                page.category = fb_page_body["category"]
                updated_pages.append(page)
        commitAllToDB(updated_pages)
    # return der page_id's
    return new_pages

def getBusinessAccounts(access_token, page):
    _fields = r"instagram_business_account{followers_count, profile_picture_url, username},followers_count"
    db_bzaccs = db.session.execute(db.select(IGBusinessAccount).filter(IGBusinessAccount.page.has(id=page.id))).scalars().all()
    new_bz_accs = []
    
    bs_res = _getInstagramData(access_token, f"/{page.fb_id}", fields=_fields)
    payload = []
    for p in bs_res:
        #print(multi_pages)
        payload.append({"method" : "GET", "relative_url": f"{p['id']}?fields="+_fields})
    bs_res = _batchRequest(access_token, payload)
    
    db_bzacc_dict = dict([(bz.fb_id, bz) for bz in db_bzaccs])
    fb_bzacc_dict = dict([(bz["instagram_business_account"]["id"], (bz,etag)) for bz,etag in bs_res])
    
    deletable_bzacc_ids, updateable_bzacc_ids, new_bzacc_ids = _findIDDifferences(db_bzacc_dict, fb_bzacc_dict, len(db_bzaccs) > 0)

    # aus der Antwort neue BZ_Accs erstellen
    for id in new_bzacc_ids:
        bz = fb_bzacc_dict[id][0]
        new_bz_acc = IGBusinessAccount(fb_id=bz["instagram_business_account"]["id"], followers_count=bz["instagram_business_account"]["followers_count"],etag=fb_bzacc_dict[id][1])
        page.business_accounts.append(new_bz_acc)
        page.followers_count = bz["followers_count"]
        
        new_bz_accs.append(new_bz_acc)
    
    commitAllToDB(new_bz_accs + [page])    
    
    if len(deletable_bzacc_ids) > 0:
        db_deletable_bzaccs = [b for b in db_bzaccs if b.fb_id in deletable_bzacc_ids]
        deleteFromDB(db_deletable_bzaccs)
        
    updated_bzaccs = []
    if len(updateable_bzacc_ids) > 0:
        db_updateable_bzaccs = [m for m in db_bzaccs if m.fb_id in updateable_bzacc_ids]
        for bz in db_updateable_bzaccs:
            fb_bzacc_body = fb_bzacc_dict[bz.fb_id]
            if fb_bzacc_body is not None:
                bz.followers_count = fb_bzacc_body["instagram_business_account"]["followers_count"]
                bz.customer.profile_picture_url = fb_bzacc_body["instagram_business_account"]["profile_picture_url"]
                bz.customer.name= fb_bzacc_body["instagram_business_account"]["username"]
                updated_bzaccs.append(bz)
        commitAllToDB(updated_bzaccs)

    return new_bz_accs

def updateCommentTimestamps(access_token, medias):
    _fields = r"replies.limit(1){timestamp},timestamp,media"
    payload, updated_medias = [], []
    
    for m in medias:
        #payload.append({"method":"GET", "relative_url": f"{m.fb_id}/comments?fields="+_fields, "headers" : [f'If-None-Match: {m.etag}']})
        payload.append({"method":"GET", "relative_url": f"{m.fb_id}/comments?fields="+_fields})

    media_res = _batchRequest(access_token, payload)
    for res in media_res:
        # wenn data nicht befüllt ist, hat der Post keine kommentare
        if len(res[0]["data"]) == 0:
            continue
        
        #print(res[0])
        # ansonsten die timestamps aus dem DB objekt nehmen und mit den Kommentaren abgleichen
        media = next((m for m in medias if m.fb_id == res[0]["data"][0]["media"]["id"]), None)
        latest_comment_timestamp = media.latest_comment_timestamp
        # oldest_comment_timestamp = media.oldest_comment_timestamp
        
        for comment in res[0]["data"]:
            # wenn es replies gibt, dann ist das oberste reply am wichtigsten
            if "replies" in comment:
                current_comment_timestamp = date_parser.isoparse(comment["replies"]["data"][0]["timestamp"])
            else:
                current_comment_timestamp = date_parser.isoparse(comment["timestamp"])
            
            if latest_comment_timestamp is None or current_comment_timestamp < latest_comment_timestamp:
                latest_comment_timestamp = current_comment_timestamp
            
            # if oldest_comment_timestamp is None or current_comment_timestamp > oldest_comment_timestamp: 
            #     oldest_comment_timestamp = current_comment_timestamp
        media.latest_comment_timestamp = latest_comment_timestamp
        updated_medias.append(media)
    commitAllToDB(updated_medias)
    
def getMedia(access_token, bz_acc):
    _fields = "media_url,timestamp,permalink,comments_count,like_count,caption,media_type,thumbnail_url"
    db_medias = db.session.execute(db.select(IGMedia).filter(IGMedia.bzacc.has(id=bz_acc.id))).scalars().all()
    new_medias = []
    
    # zuerst alle IG Media IDs sammeln
    res = _getInstagramData(access_token, f"/{bz_acc.fb_id}/media")
    
    # Batch Request an Meta API mit allen Media_IDs
    payload = []
    for m in res:
        payload.append({"method" : "GET", "relative_url": f"{m['id']}?fields="+_fields})
    media_res = _batchRequest(access_token, payload)
    
    db_media_dict = dict([(m.fb_id, m) for m in db_medias])
    fb_media_dict = dict([(m["id"], (m, etag)) for m, etag in media_res])
    
    deletable_media_ids, _, new_media_ids = _findIDDifferences(db_media_dict, fb_media_dict, len(db_medias) > 0)
    
    for id in new_media_ids:
        etag = fb_media_dict[id][1]
        body = fb_media_dict[id][0]
        new_media = IGMedia(timestamp=date_parser.isoparse(body["timestamp"]), 
                            permalink=body["permalink"],  
                            fb_id=body["id"],
                            like_count=body["like_count"],
                            comments_count=body["comments_count"],
                            caption=body["caption"],
                            media_type=body["media_type"],
                            etag=etag)
        
        if "thumbnail_url" in body:
            new_media.media_url = body["thumbnail_url"]
        else:
            new_media.media_url = body["media_url"]
        
        new_medias.append(new_media)
        bz_acc.medias.append(new_media)
    
    commitAllToDB(new_medias + [bz_acc])
    
    if len(deletable_media_ids) > 0:
        db_deletable_medias = [m for m in db_medias if m.fb_id in deletable_media_ids]
        deleteFromDB(db_deletable_medias)
    
    updateable_media_ids = _findMediasWithNewEtag(db_media_dict, fb_media_dict)
    updated_medias = []
    if len(updateable_media_ids) > 0:
        db_updateable_medias = [m for m in db_medias if m.fb_id in updateable_media_ids]
        for media in db_updateable_medias:
            etag = fb_media_dict[media.fb_id][1]
            fb_media_body = fb_media_dict[media.fb_id][0]
            if fb_media_body is not None:
                if etag != media.etag:
                    media.etag=etag
                    new_medias.append(media)
                media.timestamp=date_parser.isoparse(fb_media_body["timestamp"])
                media.permalink=fb_media_body["permalink"]
                media.fb_id=fb_media_body["id"]
                media.like_count=fb_media_body["like_count"]
                media.comments_count=fb_media_body["comments_count"]
                media.caption=fb_media_body["caption"]
                media.media_type=fb_media_body["media_type"]
                
                if "thumbnail_url" in fb_media_body:
                    media.media_url = fb_media_body["thumbnail_url"]
                else:
                    media.media_url = fb_media_body["media_url"]
                updated_medias.append(media)
                
    commitAllToDB(updated_medias)
    updateCommentTimestamps(access_token, updated_medias+new_medias)
    return new_medias
    
def getComments(access_token, media):
    _fields = "replies{from,parent,timestamp,username,text,like_count},id,timestamp,from,text,like_count"
    db_comments = db.session.execute(db.select(IGComment).filter(IGComment.media.has(id=media.id))).scalars().all()

    res = _getInstagramData(access_token, f"/{media.fb_id}/comments")
    
    payload = []
    
    for com in res:
        payload.append({"method": "GET", "relative_url": f"{com['id']}?fields=" + _fields})
    com_res = _batchRequest(access_token, payload)
    
    comment_customer, new_comments = [], []

    db_comment_dict = dict([(c.fb_id, c) for c in db_comments])
    fb_comment_dict = dict()
    for c in com_res:
        fb_comment_dict[c["id"]] = (c, False, None)
        if "replies" in c:
            for r in c["replies"]["data"]:
                fb_comment_dict[r["id"]] = (r, True, c["id"])
                
    deletable_comment_ids, updateable_comment_ids, new_comment_ids = _findIDDifferences(db_comment_dict, fb_comment_dict, len(db_comments)>0)
    user_bzacc = media.bzacc
    # print("----")
    # print(deletable_comment_ids)
    # print(updateable_comment_ids)
    # print(new_comment_ids)
    for id in new_comment_ids:
        new_comments = []
        (fb_com, is_reply, parent_id) = fb_comment_dict[id]
        # Replies werden nur zusammen mit dem Top Level Kommentar neu erstellt, ansonsten muss das bestehende objekte aus der DB geholt werden
        if is_reply:
            parent = db.session.execute(db.select(IGComment).filter(IGComment.fb_id == parent_id)).scalar_one_or_none()
            if parent is not None:
                reply = IGComment(timestamp=date_parser.isoparse(fb_com["timestamp"]), fb_id=fb_com["id"], text=fb_com["text"], like_count=fb_com["like_count"])
                comment_customer.append((reply, fb_com["from"]))
                #commitAllToDB([reply])
                reply.parent = parent
                new_comments.append(reply)
        else:
            new_comm = IGComment(timestamp=date_parser.isoparse(fb_com["timestamp"]), fb_id=fb_com["id"], text=fb_com["text"], like_count=fb_com["like_count"])
            
            comment_customer.append((new_comm, fb_com["from"]))
            new_comments.append(new_comm)
            if "replies" in fb_com:
                for r in fb_com["replies"]["data"]:
                    reply = IGComment(timestamp=date_parser.isoparse(r["timestamp"]), fb_id=r["id"], text=r["text"], like_count=r["like_count"])
                    comment_customer.append((reply, r["from"]))
                    reply.parent = new_comm
                    new_comments.append(reply)
                    
    commitAllToDB(new_comments)
  
    for comment, fb_user in comment_customer:
        db_customer = db.session.execute(db.select(IGCustomer).filter_by(fb_id=fb_user["id"])).scalar_one_or_none()
                
        if db_customer is None:
            db_customer = IGCustomer(fb_id=fb_user["id"], name=fb_user["username"])
            commitAllToDB([db_customer])
            
        # Wenn das Kommentar ein TL Kommentar ist, neuen Thread erstellen und User+Customer hier verknüpfen
        thread = None
        if comment.parent is None:
            thread = IGThread(media=media, bzacc=user_bzacc, customer=db_customer)
            
            commitAllToDB([thread])
        else:
            # Ansonsten ist das Kommentar ein reply, es muss also einen Thread bereits geben
            thread = comment.parent.thread
            
            # TL Kommentare vom User führen dazu, dass der Thread auch zum User zugeordnet wird
            # Deshalb muss bei einem reply von einem Kunden der Thread neu zugewiesen werden
            # Thread.customer sollte immer ein customer sein
            if thread.customer == user_bzacc.customer:
                thread.customer = db_customer
        
        comment.thread = thread
        comment.media = media
        comment.customer = db_customer
        
        commitAllToDB([comment, media, thread])
        thread.comments.append(comment)
        thread.is_unread = True
        media.comments.append(comment)
        db_customer.comments.append(comment)
        
    if len(deletable_comment_ids) > 0:
        db_delete_targets = []
        db_deletable_comments = [c for c in db_comments if c.fb_id in deletable_comment_ids]
        for comment in db_deletable_comments:
            if len(comment.thread.comments) == 1:
                db_delete_targets.append(comment.thread)
        deleteFromDB(db_deletable_comments + db_delete_targets)
    
    updated_comments = []
    if len(updateable_comment_ids) > 0:
        db_updateable_comments = [c for c in db_comments if c.fb_id in updateable_comment_ids]
        for com in db_updateable_comments:
            #print(fb_comment_dict[com.fb_id])
            (fb_com_body,_, _) = fb_comment_dict[com.fb_id]
            if fb_com_body is not None:
                com.text = fb_com_body["text"]
                com.timestamp = date_parser.isoparse(fb_com_body["timestamp"])
                com.like_count = fb_com_body["like_count"]
                updated_comments.append(com)
                #com.thread.is_unread = True
        
    commitAllToDB([media] + updated_comments)
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
    
    commitAllToDB([media])
    return
    
def updateInteractions(access_token, thread_ids):
    threads = db.session.execute(db.select(IGThread).filter(IGThread.id.in_(thread_ids))).scalars().all()
    bzaccs = [t.media.bzacc for t in threads]
    
    updated_medias = []
    for bz in bzaccs:
        updated_medias.extend(getMedia(access_token, bz))
        
    for media in updated_medias:
        getComments(access_token, media)
    
    for t in threads:
        getComments(access_token, t.media)
        
def connectCustomerBusinessAccounts(access_token, bz_accs):
    bz_acc_set = dict([(b.fb_id, b) for b in bz_accs])
    customers = db.session.execute(db.select(IGCustomer).filter(IGCustomer.fb_id.in_(bz_acc_set.keys()))).scalars().all()
    connected = []
    for c in customers:
        bz_acc = bz_acc_set[c.fb_id]
        bz_acc.customer = c
        connected.append(bz_acc)
    commitAllToDB(connected)
    
    print("Customer - Business-Account relationship created")
    
def updateAllEntries(access_token, user):
    pages, bz_accs, medias, comments = [], [], [], []
    
    pages = getPages(access_token, user)
    if len(pages) == 0:
        pages.extend(db.session.execute(db.select(IGPage).filter(IGPage.user.has(id=user.id))).scalars().all())
    for p in pages:
        bz_accs.extend(getBusinessAccounts(access_token, p))
    
    print("pages done")
    
    if len(bz_accs) == 0:
        for p in pages:
            bz_accs.extend(db.session.execute(db.select(IGBusinessAccount).filter(IGBusinessAccount.page.has(id=p.id))).scalars().all())
    for b in bz_accs:
        medias.extend(getMedia(access_token, b))
        
    print("bzacc done")
    
    if len(medias) == 0:
        for b in bz_accs:
            medias.extend(db.session.execute(db.select(IGMedia).filter(IGMedia.bzacc.has(id=b.id))).scalars().all())
    for m in medias:
        getComments(access_token, m)

    print("media + comments done")
    
    #connectCustomerBusinessAccounts(access_token, bz_accs)
    