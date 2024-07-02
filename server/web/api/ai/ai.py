from flask import (
    Blueprint, jsonify, request, session, current_app
)
from flask_login import login_required, current_user
from ....db.models import OpenAIRun, IGMedia, db
from ....db import db_handler
from ....utils import assistant_utils as gpt_assistant
import traceback, json, os, requests
from ...tasks import generate_response, loadCachedResults

def GPTConfig():
    from server import GPTConfig
    return GPTConfig

ai_bp = Blueprint('ai_bp', __name__)

@ai_bp.route("/generate_responses", methods=["POST"])
@login_required
def generate_responses():
    try:
        # ThreadID raussuchen
        body = request.get_json()
        if "threadId" not in body or body["threadId"] == "":
            return jsonify({"error":"No threadId specified in request"}), 500

        # # Prüfen, ob Thread mit User verknüpft ist
        # if not isThreadByUser(body["threadId"], current_user):
        #     return jsonify({"error":"Thread not associated with user"}), 500
        
        cached_data = loadCachedResults(current_user.oauth.token["access_token"], current_user.id)
        run, gpt_thread = generate_response(current_user.id , GPTConfig, cached_data["id_mapping"].get(body["threadId"]))
        
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
                return jsonify({"error":"Problem loading answers for this Thread"}), 400
        else:
            return jsonify(run.status), 400
    
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occoured"}), 500

