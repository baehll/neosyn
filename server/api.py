from flask import (
    Blueprint, jsonify, request
)
import requests
from flask_jwt_extended import jwt_required
from . import GPT_MODEL, CLIENT

api = Blueprint('api', __name__)

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
