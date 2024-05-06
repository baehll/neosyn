from flask import (
    Blueprint, jsonify, request, session, current_app
)
from operator import attrgetter
import os
import requests
from flask_login import login_required, current_user
from ...models import db, User , _PlatformEnum, Organization, OAuth, Platform, IGThread
from ....utils import assistant_utils as gpt_assistant
from ..data.threads import isThreadByUser
import traceback

def GPTConfig():
    from server import GPTConfig
    return GPTConfig

ai_bp = Blueprint('ai_bp', __name__)

@ai_bp.route("/generate_response", methods=["POST"])
@login_required
def generate_response():
    try:
        # ThreadID raussuchen
        body = request.get_json()
        if "threadId" not in body or body["threadId"] == "":
            return jsonify({"error":"No threadId specified in request"}), 500

        # Prüfen, ob Thread mit User verknüpft ist
        if not isThreadByUser(body["threadId"], current_user):
            return jsonify({"error":"Thread not associated with user"}), 500
        
        thread = db.session.execute(db.select(IGThread).filter(IGThread.id == body["threadId"])).scalar_one_or_none()
        if thread is None:
            return jsonify({"error":"No thread found"}), 500
        
        gpt_thread = None
        
        # Hat IGThread gpt_thread ?
        if thread.gpt_thread == "":
            # Wenn nicht, neuen Thread erstellen 
            gpt_thread = GPTConfig().CLIENT.beta.threads.create()
            thread.gpt_thread = gpt_thread.id
            db.session.add(thread)
            db.session.commit()
        else:
            gpt_thread = GPTConfig().CLIENT.beta.threads.retrieve(thread.gpt_thread)
        
        # Überprüfen, ob in metadata der aktuellste kommentar steht
        if "last_comment_id" not in gpt_thread.metadata:
            last_id = None
            # Alle Kommentare in diesem Thread hinzufügen
            for c in thread.comments:
                message = GPTConfig().CLIENT.beta.threads.messages.create(
                    thread_id=gpt_thread.id,
                    role="user",
                    content=c.text
                )
                last_id = c.id
            GPTConfig().CLIENT.beta.threads.update(
                gpt_thread.id,
                metadata={
                    "last_comment_id":str(last_id)
                })
        else:
            last_comment = max(thread.comments, key=attrgetter("id"))
            if gpt_thread.metadata["last_comment_id"] != last_comment.id:
                # Alle Kommentare zwischen alter last_comment_id und last_comment.id zu messages hinzufügen
                for c in [t for t in thread.comments if t.id >= gpt_thread.metadata["last_comment_id"]]:
                    message = GPTConfig().CLIENT.beta.threads.messages.create(
                        thread_id=gpt_thread.id,
                        role="user",
                        content=c.text
                    )
                GPTConfig().CLIENT.beta.threads.update(
                    gpt_thread.id,
                    metadata={
                        "last_comment_id":str(last_comment.id)
                    }
                )
        # Antworten Generieren
        orga = db.session.execute(db.select(Organization).filter(Organization.users.any(id=current_user.id))).scalar_one_or_none()
        
        run = GPTConfig().CLIENT.beta.threads.runs.create(
            thread_id=gpt_thread.id,
            assistant_id=orga.assistant_id,
            instructions=""
        )
        print(run)
        if run.status == 'completed': 
            messages = GPTConfig().CLIENT.beta.threads.messages.list(
                thread_id=thread.id
            )
            print(messages)
        else:
            print(run.status)
        return jsonify()
    
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occoured"}), 500

