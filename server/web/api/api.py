from flask import (
    Blueprint, jsonify, request, session, current_app
)
import os
import requests
from flask_login import login_required, current_user
from decouple import config
from ..models import db, User , _PlatformEnum, Organization, OAuth, Platform, IGThread, File
from pathvalidate import replace_symbol
from ...utils import file_utils, IGApiFetcher, assistant_utils
from werkzeug.utils import secure_filename
import traceback
from .data.threads import isThreadByUser
from ..tasks import init_assistant

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
        
        if current_user.organization is not None:
            return jsonify({"error": "User already associated with organization"}), 500
        
        # Neues Organization DB Objekt initialisieren
        new_orga = Organization(name=form_data["companyname"])
        
        # User updaten, verknüpft mit Orga
        new_orga.users.append(current_user)
        current_user.name = form_data["username"]
        
        logo = None
        
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
            
            logo = File(filename=filename, data=file.read())
            logo.organization = new_orga
            db.session.add(logo)
            
        if logo is not None:
            new_orga.logo_id = logo.id
            db.session.add(new_orga)
            
        db.session.add(new_orga)
        db.session.add(current_user)
        db.session.commit()
        
        return jsonify(), 200
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occurred"}), 500

@api_bp.route("/company_files", methods=["POST"])
@login_required
def company_files():
    try:
        # für jeweilige Organisation von User Upload Ordner laden
        orga = db.session.execute(db.select(Organization).filter(Organization.users.any(id=current_user.id))).scalar_one_or_none()
        if orga is None:
            return jsonify({"error":"No Organization for User found"}), 500
        
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
                
                new_file = File(filename=filename, data=file.read())
                orga.files.append(new_file)
                new_file.organization = orga
                successful.append(filename)
                db.session.add(new_file)
            
            db.session.add(orga)
            db.session.commit()

            init_assistant.delay(orga.id)
            
            if len(errors) > 0:
                return jsonify({"error": errors, "successful":", ".join(successful) }), 422
            else:
                return jsonify({"successful":", ".join(successful)}), 200
        else:
            db.session.add(orga)
            db.session.commit()
            init_assistant.delay(orga.id)
            return jsonify(), 200
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occured"}), 500
    
@api_bp.route("/me", methods=["GET"])
@login_required
def me():
    try:
        return jsonify({
            "logoURL": "",
            "name": "",
            "companyName": ""
        }), 200
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occoured"}), 500
    
@api_bp.route("/update_all_entries", methods=["GET"])
@login_required
def update_all_entries():
    oauth = db.session.execute(db.select(OAuth).filter(OAuth.user.has(id=current_user.id))).scalar_one_or_none()
    IGApiFetcher.updateAllEntries(oauth.token["access_token"], current_user)
    return jsonify({}), 200