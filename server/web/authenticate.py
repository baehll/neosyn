from flask import (
    Blueprint, jsonify, request, current_app
)
from blinker import signal
from decouple import config
from datetime import timedelta
from .models import db, User
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token


authenticate = Blueprint('authenticate', __name__)

@authenticate.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    # Nach User in DB suchen
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        # JWToken generieren mit user infos
        token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
        print(token)
        return jsonify({'token': token})
    else:
        return jsonify({'message': 'Invalid Credentials'}), 401
    
@authenticate.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    try:
        #print(get_jwt_identity())
        user_logged_out = signal('user_logged_out')
        user_logged_out.send(current_app, jwt_payload=get_jwt_identity())
        return jsonify({"msg":"Successful"})
    except:
        print("error on logout")
        return jsonify({"msg":"Unsuccessful"})