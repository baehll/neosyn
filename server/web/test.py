from flask import (
    Blueprint, jsonify, request, current_app
)
from blinker import signal
from decouple import config
from datetime import timedelta
from .models import db, UserToken
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token
from ..workers.IGApiWorker import getPages, getComments, getBusinessAccounts, getMedia

test = Blueprint('test', __name__)

@test.route("/pages", methods=["GET"])
@jwt_required()
def pages():
    # Access Token extrahieren von User
    #print(get_jwt_identity())
    usertoken = db.session.execute(db.select(UserToken).filter_by(user_id=get_jwt_identity())).scalar_one_or_none()
    
    if usertoken is not None:
        # Worker anschmeißen
        results = getPages(usertoken.client_token, usertoken)
        # return mit Status
        return jsonify({"results": results}) 
    else:
        return jsonify()

@test.route("/bz_acc", methods=["GET"])
def bz_acc():
    return {} 

@test.route("/medias", methods=["GET"])
def medias():
    return {} 

@test.route("/comments", methods=["GET"])
def comments():
    return {} 