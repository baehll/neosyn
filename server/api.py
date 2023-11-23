from flask import (
    Blueprint, jsonify, request
)
import requests
import jwt

from . import GPT_MODEL, CLIENT

api = Blueprint('api', __name__)

@api.route("/fast_response", methods=["POST"])
def fast_response():
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
