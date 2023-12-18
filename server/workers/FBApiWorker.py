from ..web.models import db, Page, Business_Account, Media, Comment, UserTokenPageAssociation
import requests

_URL = "https://graph.facebook.com/v18.0"
# _TASKS = ["ADVERTISE", "ANALYZE", "CREATE_CONTENT", "MESSAGING", "MODERATE", "MANAGE"]

def getPages(access_token, usertoken):
    page_ids = []
    # request gegen IG Graph API
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
                        
                # mit UserToken verknüpfen und ETag setzen
                usertoken.pages.append(new_page)
                page_ids.append(page["id"])
                
                db.session.add(new_page)
                
            db.session.add(usertoken)
            
            # commit
            db.session.commit()
        except:
            # Rollback on Error
            db.session.rollback()
        finally:
            db.session.close()
        
    # return der page_id's
    return page_ids

def getBusinessAccounts():
    pass

def getMedia():
    pass

def getComments():
    pass