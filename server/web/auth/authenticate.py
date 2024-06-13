from flask import (
    Blueprint, jsonify, request, current_app, send_from_directory, redirect, session
)
from flask_login import current_user, login_user, login_required, logout_user
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound
from ...db import db, User, OAuth, EarlyAccessKeys, Platform
from ...auth_blueprint import FB_Blueprint
import traceback
from ..tasks import loadCachedResults
from ...social_media_api import IGApiFetcher

authenticate = FB_Blueprint.make_facebook_blueprint(
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user),
    config_id="1002221764623878"
)

@authenticate.route("/early_access", methods=["POST"])
def early_access():
    try:
        access_key = request.get_json()["access_key"]
        
        if access_key is None or access_key == "":
            return jsonify({"error": "No access_key specified or missing in request"}), 400
        
        keys = db.session.execute(db.select(EarlyAccessKeys)).scalars()
        
        for saved_key in keys:
        # Abgleich von Key mit Einträgen in Secret_Access Tabelle
            if saved_key.check_key(access_key):
                return jsonify({}), 200
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occurred"}), 500
    return jsonify({}), 400

@authenticate.route("/early_access_redirect", methods=["POST"])
def early_access_redirect():
    try:
        access_key = request.get_json()["access_key"]
        
        if access_key is None or access_key == "":
            return jsonify({"error": "No access_key specified or missing in request"}), 400
        
        keys = db.session.execute(db.select(EarlyAccessKeys)).scalars()
        
        for saved_key in keys:
        # Abgleich von Key mit Einträgen in Secret_Access Tabelle
            if saved_key.check_key(access_key):
            # Bei richtigen Key: login.html redirect
                return send_from_directory("static", "login.html")
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occurred"}), 500
    return jsonify({}), 400


@authenticate.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@authenticate.route("/debug_login/<id>")
def debug_login(id):
    if current_app.debug == True:
        instagram_platform = Platform.query.filter_by(name="Instagram").one()
        user = User(platform=instagram_platform)
        oauth = OAuth.query.filter_by(id=int(id)).one()
        oauth.user = user
        db.session.add_all([oauth, user])
        db.session.commit()
        login_user(user)
        IGApiFetcher.updateAllEntries(user.oauth.token["access_token"], user)
        return redirect("/registration.html")
    else:
        return jsonify(), 404

@oauth_authorized.connect_via(authenticate)
def facebook_logged_in(blueprint, token):
    if not token:
        print("Failed to log in.")
        return False

    resp = blueprint.session.get("/me")
    if not resp.ok:
        msg = "Failed to fetch user info."
        print(msg)
        return False

    info = resp.json()
    user_id = info["id"]

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(provider=blueprint.name, provider_user_id=user_id)
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, provider_user_id=user_id, token=token)

    if oauth.user:
        login_user(oauth.user)
        # trigger async DB Update
        # init = loadCachedResults(oauth.token["access_token"], f"media_trees_{oauth.user_id}")
        # init.forget()
        print("Successfully signed in.")
        return redirect("/app.html")
    else:
        instagram_platform = Platform.query.filter_by(name="Instagram").one()
        # Create a new local user account for this user
        user = User(platform=instagram_platform)
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
        print("New User created and successfully signed in.")
        
        # init = loadCachedResults(oauth.token["access_token"], f"media_trees_{oauth.user_id}")
        # init.forget()
        
        return redirect("/registration.html")
    
    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False

# notify on OAuth provider error
@oauth_error.connect_via(authenticate)
def facebook_error(blueprint, error, error_description, error_uri):
    msg = ("OAuth error from {name}! " "message={error} error_description={error_description}, error_uri={error_uri}").format(
        name=blueprint.name, error=error, error_description=error_description, error_uri=error_uri
    )
    print(msg)
    return redirect("/login.html")