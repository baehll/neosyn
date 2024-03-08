from flask import (
    Blueprint, jsonify, request, session
)
import requests
from flask_login import login_required
from decouple import config
from ..models import db, User , _PlatformEnum

api = Blueprint('api', __name__)

def GPTModel():
    from server import chatGPTModel
    return chatGPTModel()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"txt", "pdf"}

@api.route("/init_user", methods=["POST"])
@login_required
def init_user():
    # Neues Organization DB Objekt initialisieren
    # Neuen User initialisieren, verknüpft mit Orga und flask_dance_oauth Objekt
    # upload ordner für Orga erstellen, Pfad für Orga speichern
    # Logo im upload ordner abspeichern
    return jsonify({}) 

@api.route("/company_files", methods=["POST"])
@login_required
def company_files():
    # für jeweilige Organisation von User Upload Ordner laden
    # alle angehängten Files auf richtiges Dateiformat überprüfen
    # abspeichern im Upload Ordner
    
    return jsonify({}) 

@api.route("/long_lived_access", methods=["POST"])
@login_required
def long_lived_access():
    print(request.get_json())
    # Erst einen long lived access token generieren
    url = 'https://graph.facebook.com/v18.0/oauth/'
    params = {
        "client_id": config("FB_APP_ID"),
        "client_secret": config("FB_CLIENT_SECRET"),
        "fb_exchange_token": request.get_json()["access_token"],
        "grant_type": "fb_exchange_token"
    }
    res = requests.get(url + "access_token", params=params)
    
    # Wenn es einen Token gibt, wird ein long lived client token versucht zu generieren
    if(res.status_code == 200):
        params = {
            "client_id": config("FB_APP_ID"),
            "client_secret": config("FB_CLIENT_SECRET"),
            "access_token": res.json()["access_token"],
            "redirect_uri": "https://quiet-mountain-69143-51eb8184b186.herokuapp.com/"
        }
        resp = requests.get(url + "client_code", params=params)
        
        #Wenn der Code generiert wurde, wird das ans Frontend geschickt und von dort weiter gemacht
        if(resp.json()["code"]):
            return jsonify({"code": resp.json()["code"]})
          
# @api.route("/long_lived_client_token", methods=["POST"])
# def long_lived_client_token():
#     #den richtigen Nutzer finden und die Session dafür befüllen
#     user = db.session.execute(db.select(User).filter_by(id=get_jwt_identity())).scalar_one_or_none()
    
#     if user is None:
#         return jsonify({"error": "No user found for request"}), 404
#     else:
#         ut = db.session.execute(db.select(UserToken).filter_by(user_id=get_jwt_identity())).scalar_one_or_none()
#         if ut is None:
#             tokenEntity = UserToken(expiration=request.get_json()["expiration"], client_token=request.get_json()["access_token"], user=user, platform=request.get_json()["platform"])
#             db.session.add(tokenEntity)
#             db.session.commit()
#             return jsonify({}), 201 
#         else:
#             ut.set_data(exp=request.get_json()["expiration"], token=request.get_json()["access_token"], platform=request.get_json()["platform"])
#             db.session.add(ut)
#             db.session.commit()
#             return jsonify({}), 202
    

@api.route("/fast_response", methods=["POST"])
@login_required
def fast_response():
    print(request.get_json())
    comment = request.get_json()["comment"]
    prompt = f'''
        Generiere 5 Antworten auf das folgende Kommentar, als wärst du ein Social Media Manager für ein Unternehmen.
        Antworte ausschließlich in Form eines Arrays, in dem die einzelnen Antworten Elemente des Arrays darstellen. 
        Das Array soll so strukturiert sein, dass es von Javascript als Array erkannt wird.
        user: {comment}
        bot:
    '''
    response = GPTModel()["CLIENT"].chat.completions.create(
        model = GPTModel()["GPT_MODEL"],
        messages=[{'role': 'user', 'content': prompt}]
    )
    output = response.choices[0].message.content.split("\"")[1::2]
    print(output)
    return jsonify({"answers": output})

@api.route("/context_response", methods=["POST"])
@login_required
def context_response():
    comment_line = ""
    if(request.get_json()["comment"] != ""):
        comment_line = f'Kommentar: {request.get_json()["comment"]}'

    prompt = f'''
        Generiere eine Antwort auf folgenden Social Media Beitrag:
        Bild URL: {request.get_json()["media_url"]}
        Beitrag: {request.get_json()["caption"]}
    '''

    prompt = prompt + comment_line + '''
        Deine Antwort soll sich auf das Bild in der URL, den Beitrag sowie das Kommentar (falls vorhanden) beziehen.
        Antworte mit einem unformatierten String 
    '''

    response = GPTModel()["CLIENT"].chat.completions.create(
        model = GPTModel()["GPT_MODEL"],
        messages=[{'role': 'user', 'content': prompt}]
    )

    return jsonify({"answer": response.choices[0].message.content})
