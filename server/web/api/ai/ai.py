from flask import (
    Blueprint, jsonify, request, session, current_app
)
from operator import attrgetter
from flask_login import login_required, current_user
from ...models import db, User , _PlatformEnum, Organization, OAuth, Platform, IGThread, OpenAIRun
from ....utils import assistant_utils as gpt_assistant
from ..data.threads import isThreadByUser
import traceback, json, os, requests


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
        
        gpt_thread = GPTConfig().CLIENT.beta.threads.retrieve(current_user.organization.gpt_thread_id)
        
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
                for c in [t for t in thread.comments if t.id >= int(gpt_thread.metadata["last_comment_id"])]:
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
        run = GPTConfig().CLIENT.beta.threads.runs.create_and_poll(
            thread_id=gpt_thread.id,
            assistant_id=current_app.config["GPT_ASSISTANT_ID"],
            instructions=open(os.path.join(current_app.config["CONFIG_FOLDER"], "instruction_template.txt"),"r", encoding="utf-8").read()
        )
        db_run = OpenAIRun(run_id=run.id, organization=current_user.organization)
        
        db.session.add(db_run)
        db.session.commit()
        
        if run.status == 'completed': 
            messages = GPTConfig().CLIENT.beta.threads.messages.list(
                thread_id=gpt_thread.id,
                run_id=run.id,
                order="asc"
            )
            try:
                message_arr = json.loads(messages.data[0].content[0].text.value)
                #print(message_arr)
                return jsonify(message_arr), 200
            except:
                return jsonify({"error":"Problem generating answers for this Thread"}), 400
        else:
            return jsonify(run.status), 400
    
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occoured"}), 500

