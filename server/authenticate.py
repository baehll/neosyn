from flask import (
    Blueprint, jsonify, request
)
import requests
import jwt
from decouple import config
from datetime import datetime, timedelta
from .models import db, User

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

authenticate = Blueprint('authenticate', __name__)

@authenticate.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    # Nach User in DB suchen
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        # JWToken generieren mit user infos
        token = jwt.encode({
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(days=1)
        }, config("JWT_SECRET_TOKEN"))
        
        return jsonify({'token': token})
    else:
        return jsonify({'message': 'Invalid Credentials'}), 401