from flask import (
    Blueprint, jsonify, request, session, current_app
)
import os
import requests
from flask_login import login_required, current_user
from decouple import config
from ..models import db, User , _PlatformEnum, Organization, OAuth, Platform, IGThread
from pathvalidate import replace_symbol
from ...utils import file_utils, IGApiFetcher, assistant_utils
from werkzeug.utils import secure_filename
import traceback
from .data.threads import isThreadByUser

api_bp = Blueprint('api', __name__)

@api_bp.route("/supported_platforms", methods=["GET"])
@login_required
def supported_platforms():
    try:
        platforms = db.session.execute(db.select(Platform)).scalars().all()
        result = []
        for p in platforms:
            result.append({
                "name": p.name.name,
                "is_implemented": p.is_implemented,
                "id": p.id
            })
        return jsonify(result), 200
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occurred"}), 500

@api_bp.route("/init_user", methods=["POST"])
@login_required
def init_user():
    try:
        form_data = request.form
        
        if "username" not in form_data or form_data["username"] == "":
            return jsonify({"error": "No username specified"}), 400
        
        if "companyname" not in form_data or form_data["companyname"] == "":
            return jsonify({"error": "No companyname specified"}), 400
        
        # Neues Organization DB Objekt initialisieren
        new_orga = Organization(name=form_data["companyname"])
        
        # User updaten, verknüpft mit Orga
        new_orga.users.append(current_user)
        current_user.name = form_data["username"]
        # aus companyname einen ordner ableiten
        new_folder = replace_symbol(form_data["companyname"].upper() + "/")
        
        upload_folder_path = os.path.join(current_app.config["UPLOAD_FOLDER"], new_folder)
        
        # Upload Ordner Name sollte abhängig von Orga ID in DB sein ??
        # upload ordner für Orga erstellen, Pfad für Orga speichern
        if os.path.exists(upload_folder_path):
            return jsonify({"error": f"Folder already exists for companyname {form_data['companyname']}, path: '{new_folder}'"}), 500
        else:
            os.makedirs(upload_folder_path)
            new_orga.folder_path = new_folder
        
        # Logo im upload ordner abspeichern
        if 'file' in request.files:
            file = request.files["file"]
            if file.filename == "":
                return jsonify({"error":"File attached, but no filename specified"}), 500
            if not file_utils.allowed_logo_extensions(file.filename):
                return jsonify({"error": f"File Extension not allowed, must be {', '.join(file_utils.ALLOWED_LOGO_EXTENSIONS)}"}), 500
            
            filename = secure_filename(file.filename)
            if filename == "":
                return jsonify({"error":"Filename invalid"}), 500
            
            file.save(os.path.join(upload_folder_path, filename))
            new_orga.logo_file = filename
            
        db.session.add(new_orga)
        db.session.add(current_user)
        db.session.commit()
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occurred"}), 500
    return jsonify({}), 200

@api_bp.route("/company_files", methods=["POST"])
@login_required
def company_files():
    try:
        # für jeweilige Organisation von User Upload Ordner laden
        orga = db.session.execute(db.select(Organization).filter(Organization.users.any(id=current_user.id))).scalar_one_or_none()
        if orga is None:
            return jsonify({"error":"No Organization for User found"}), 500
        elif orga.folder_path == "":
            return jsonify({"error":"No Organization Folder defined"}), 500  
        
        upload_folder_path = os.path.join(current_app.config["UPLOAD_FOLDER"], orga.folder_path)
        
        if request.files:
            errors = []
            successful = []
            if len(request.files.getlist("files[]")) > 8:
                return jsonify({"error":"Too many files, only 8 allowed"}), 500
            
            for file in request.files.getlist("files[]"):
                filename = secure_filename(file.filename)
                # alle angehängten Files auf richtiges Dateiformat, Dateiname, Dateigröße überprüfen
                if filename == "":
                    errors.append(f"Invalid filename, {file.filename}")
                    continue
                
                if not file_utils.allowed_company_file_extensions(filename):
                    errors.append(f"File Extension not allowed, {file.filename}")
                    continue
                
                filesize = file_utils.get_file_size(file)
                if filesize > current_app.config["MAX_FILE_SIZE"]:
                    errors.append(f"File {file.filename} too big, only {current_app.config['MAX_FILE_SIZE']} allowed ({filesize})")
                    continue
                
                # abspeichern im Upload Ordner
                file.save(os.path.join(upload_folder_path, filename))
                successful.append(file.filename)
            
            assistant_utils.init_assistant(config("COMPANY_FILE_UPLOAD_FOLDER"), successful, orga)
            
            db.session.add(orga)
            db.session.commit()
            
            if len(errors) > 0:
                return jsonify({"error": errors, "successful":", ".join(successful) }), 422
            else:
                return jsonify({"successful":", ".join(successful)}), 200

        return jsonify({}), 200
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occoured"}), 500
  
@api_bp.route("/data/threads/<id>/post", methods=["GET"])
@login_required
def get_post_information(id):
    try:
        if not isThreadByUser(int(id), current_user):
            return jsonify(), 204
        
        # jeweiliges media objekt raussuchen und zurückgeben
        thread = db.session.execute(db.select(IGThread).filter(IGThread.id == id)).scalar_one_or_none()
        
        if thread is None:
            return jsonify({"error":"No thread with the specified ID found"})

        return jsonify({
            "id": thread.media.id,
            "threadId": thread.id,
            "permalink": thread.media.permalink,
            "mediaType": thread.media.media_type,
            "postMedia": thread.media.media_url,
            "postContent": thread.media.caption,
            "platform": _PlatformEnum.Instagram.name,
            "likes": thread.media.like_count,
            "comments": thread.media.comments_count,
            "shares": None,
            "timestamp": thread.media.timestamp
        })
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occoured"}), 500