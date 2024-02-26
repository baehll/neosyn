from flask import (
    Blueprint, jsonify, request, current_app
)
from blinker import signal
from decouple import config
from datetime import timedelta
from .models import db, User

authenticate = Blueprint('authenticate', __name__)


@authenticate.route("/meta_redirect", methods=["POST", "GET"])
def login():
    '''
        Redirect URI für Meta Login. Hier wird ein access_token benötigt, mit dem eine User ID zur Identifikation eines Nutzers von Meta API abgefragt wird. 
        Aus dem access_token lassen sich langlebige Tokens ableiten, die für spätere Datenauswertungen benutzt werden. 
    '''
    data = request.get_json()
    #user_id extrahieren
    print(data)
    #user_id mit access_token in DB speichern
    return jsonify({})