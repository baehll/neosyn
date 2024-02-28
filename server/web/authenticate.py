from flask import (
    Blueprint, jsonify, request, current_app, redirect
)
from flask_login import current_user, login_user, login_required, logout_user
from flask_dance.contrib.facebook import make_facebook_blueprint
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound
from .models import db, User, OAuth

authenticate = make_facebook_blueprint(
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user)
)

@authenticate.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@oauth_authorized.connect_via(authenticate)
def facebook_logged_in(blueprint, token):
    #print("hello world")
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
        print("Successfully signed in.")

    else:
        # Create a new local user account for this user
        user = User(name=info["name"])
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
        print("Successfully signed in.")

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False

# notify on OAuth provider error
@oauth_error.connect_via(authenticate)
def facebook_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    print(msg)