from flask import Blueprint, jsonify, request, current_app
from .models import db, UserToken, Page
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token
from ..workers.IGApiWorker import getPages, getComments, getBusinessAccounts, getMedia

test = Blueprint('test', __name__)

@test.route("/pages", methods=["GET"])
@jwt_required()
def pages():
    # Access Token extrahieren von User
    usertoken = db.session.execute(db.select(UserToken).filter_by(user_id=get_jwt_identity())).scalar_one_or_none()
    
    if usertoken is not None:
        # Worker anschmeißen
        results = getPages(usertoken.client_token, usertoken)
        # return mit Status
        return jsonify({"results": [r.to_dict() for r in results]}) 
    else:
        return jsonify({"ERROR": "Usertoken returned none"})

@test.route("/bz_acc", methods=["POST"])
@jwt_required()
def bz_acc():
    usertoken = db.session.execute(db.select(UserToken).filter_by(user_id=get_jwt_identity())).scalar_one_or_none()
    
    if usertoken is not None:
        page_ids = request.get_json()["pages"]
        pages = db.session.execute(db.select(Page).filter(Page.fb_id.in_(page_ids))).scalars()
        results = []
        for p in pages:
            results.extend(getBusinessAccounts(usertoken.client_token, p))
        print(results)
        return jsonify({"results": [r.to_dict() for r in results]})
    else:
        return jsonify({"ERROR": "Usertoken returned none"})

@test.route("/medias", methods=["GET"])
@jwt_required()
def medias():
    return {} 

@test.route("/comments", methods=["GET"])
@jwt_required()
def comments():
    return {} 