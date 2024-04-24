from ..models import db, IGPage, IGBusinessAccount, IGMedia, IGComment
import requests, json
from datetime import datetime

# UTILITY FUNCTIONS UND VARIABLEN

_URL = "https://graph.facebook.com/v18.0"
# TASKS = ["ADVERTISE", "ANALYZE", "CREATE_CONTENT", "MESSAGING", "MODERATE", "MANAGE"]

# request gegen IG Graph API für die IDs (pre Batches)
def _getIDs(access_token, path, fields=""):
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
        print("ID Request GET returned " + req.status_code + f", (URL: {path}, Fields: {fields} )")
 
# Liefert eine Liste an allen Einträgen, die unter dem Path und den Fields vorhanden sind, inkl. paging results (wenn in einer Response > 25 Einträge sind)
def _getInstagramData(access_token, path, fields=""):
    ids = _getIDs(access_token, path, fields)
    results = []
    if "data" in ids:
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
                print("Paging Results GET returned " + req.status_code + f", (URL: {req_url})")
    else:
        #print(ids.json())
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
                    
                    results.append({
                            "etag": etag,
                            "body": body
                        })
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
def getPages(access_token, usertoken):
    _fields = "name,category,id,followers_count,tasks"
    # in DB nach pages für den usertoken gucken
    pages = db.session.execute(db.select(Page).filter_by(usertokens=usertoken)).scalars().all()
    new_pages = []
    
    if len(pages) == 0:
        # alle Pages des Users abfragen
        page_res = _getInstagramData(access_token, "/me/accounts", _fields)
        for p in page_res:
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
        bs_res = _getInstagramData(access_token, f"/{page.fb_id}", fields=_fields)
        
        # aus der Antwort neue BZ_Accs erstellen
        for bz in bs_res:
            new_bz_acc = BusinessAccount(fb_id=bz["instagram_business_account"]["id"], followers_count=bz["instagram_business_account"]["followers_count"])
            page.business_accounts.append(new_bz_acc)
            page.followers_count = bz["followers_count"]
            new_bz_accs.append(new_bz_acc)
        
        _getETagsForNewObjs(access_token, new_bz_accs)
        _commitToDB(new_bz_accs + [page])
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
        res = _getInstagramData(access_token, f"/{bz_acc.fb_id}/media")
        
        # Batch Request an Meta API mit allen Media_IDs
        payload = []
        for medias in res:
            for m in medias["data"]:
                payload.append({"method" : "GET", "relative_url": f"{m['id']}?fields="+_fields})
        mediaRes = _batchRequest(access_token, payload)
                
        for m in mediaRes:
            body = m["body"]
            new_media = Media(timestamp=datetime.strptime(body["timestamp"], "%Y-%m-%dT%H:%M:%S%z"), permalink=body["permalink"], media_url=body["media_url"], fb_id=body["id"])
            new_medias.append(new_media)
            bz_acc.medias.append(new_media)
        _getETagsForNewObjs(access_token, new_medias)
        _commitToDB(new_medias + [bz_acc])
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

    res = _getInstagramData(access_token, f"/{media.fb_id}/comments")
    
    # Batch Request, um an alle ETags und Daten zu kommen
    payload = []
    for com in res:
        for c in com["data"]:
            payload.append({"method": "GET", "relative_url": f"{c['id']}?fields="+_fields})
    batchRes = _batchRequest(access_token, payload)
    
    if len(comments) == 0:    
        new_comments = []
        #print("BATCH RES SIZE: " + str(len(batchRes)))
        for c in batchRes:
            body = c["body"]
            new_comm = Comment(timestamp=datetime.strptime(body["timestamp"], "%Y-%m-%dT%H:%M:%S%z"), fb_id=body["id"], from_user=body["from"]["id"])
            new_comments.append(new_comm)
            media.comments.append(new_comm)
            #print(body)
            if "replies" in body:
                #print("REPLY SIZE: " + str(len(body["replies"]["data"])))
                for r in body["replies"]["data"]:
                    #print(r)
                    reply = Comment(timestamp=datetime.strptime(r["timestamp"], "%Y-%m-%dT%H:%M:%S%z"), fb_id=r["id"], from_user=r["from"]["id"])
                    new_comm.children.append(reply)
                    new_comments.append(reply)
                    media.comments.append(reply)
        _getETagsForNewObjs(access_token, new_comments)
        _commitToDB(new_comments + [media])
        
        return new_comments
    else:        
        batch_set = set([int(b["body"]["id"]) for b in batchRes])
        comment_set = set([c.fb_id for c in comments])
        new_ids = batch_set - comment_set
        existing_and_new_ids = comments + list(new_ids)
        updated_comments = _getETagsForExistingObjs(access_token, _fields, existing_and_new_ids)
        print(updated_comments)
        # zu Updatene Einträge finden und aktualisieren
        entries = db.session.execute(db.select(Comment).filter(Comment.fb_id.in_([u["id"] for u in updated_comments ]))).scalars().all()
        _updateExistingEntries(entries, updated_comments)
        
        _commitToDB(entries) 
        return entries
    