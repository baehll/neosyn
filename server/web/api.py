from flask import (
    Blueprint, jsonify, request
)
import requests
from decouple import config
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token
from . import GPT_MODEL, CLIENT
from .models import db, User, UserToken

api = Blueprint('api', __name__)

@api.route("/long_lived_access", methods=["POST"])
@jwt_required()
def long_lived_access():
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
          
@api.route("/long_lived_client_token", methods=["POST"])
@jwt_required()
def long_lived_client_token():
    #den richtigen Nutzer finden und die Session dafür befüllen
    user = User.query.filter_by(id=get_jwt_identity()).first()
    if user is None:
        return jsonify({"error": "No user found for request"}), 404
    else:
        session = UserToken.query.filter_by(user_id=user.id).first()
        if(session):
            session.set_data(exp=request.get_json()["expiration"], token=request.get_json()["access_token"], platform=request.get_json()["platform"])
            return jsonify({}), 202
        else:
            tokenEntity = UserToken(expiration=request.get_json()["expiration"], client_token=request.get_json()["access_token"], user_id=user.id, platform=request.get_json()["platform"])
            db.session.add(tokenEntity)
            db.session.commit()
            return jsonify({}), 201 
    
@api.route("/init_acc", methods=["POST"])
@jwt_required()
def init_acc():
    user = User.query.filter_by(id=get_jwt_identity()).first()
    if user is None:
        return jsonify({"error": "No user found for request"}), 404
    else:
        user_tokens = UserToken.query.filter_by(user_id=user.id).all()
        
        for token in user_tokens:
            if token.platform == "IG_GraphAPI":
                try:
                    pass
                except:
                    pass
                
        
        

@api.route("/fast_response", methods=["POST"])
@jwt_required()
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
    response = CLIENT.chat.completions.create(
        model = GPT_MODEL,
        messages=[{'role': 'user', 'content': prompt}]
    )
    output = response.choices[0].message.content.split("\"")[1::2]
    print(output)
    return jsonify({"answers": output})

@api.route("/context_response", methods=["POST"])
@jwt_required()
def context_response():
    print(request.get_json())
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

    response = CLIENT.chat.completions.create(
        model = GPT_MODEL,
        messages=[{'role': 'user', 'content': prompt}]
    )

    return jsonify({"answer": response.choices[0].message.content})
