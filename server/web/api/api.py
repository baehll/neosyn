from flask import (
    Blueprint, jsonify, request, session, current_app, send_file
)
import base64, mimetypes
from flask_login import login_required, current_user

from ...social_media_api import IGApiFetcher
from ...db.models import db, Organization, Platform, File
from ...utils import file_utils
from werkzeug.utils import secure_filename
import traceback
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
        
        if current_user.organization is None: 
            # Neues Organization DB Objekt initialisieren
            new_orga = Organization(name=form_data["companyname"])
        
            # User updaten, verknüpft mit Orga
            new_orga.users.append(current_user)
            current_user.name = form_data["username"]
        else:
            current_user.organization.name = form_data["companyname"]
            #return jsonify({"error": "User already associated with organization"}), 500
        
        logo = None
        
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
            db.session.commit()
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

            res = init_assistant.delay(orga.id)
            res.forget()
            if len(errors) > 0:
                return jsonify({"error": errors, "successful":", ".join(successful) }), 422
            else:
                return jsonify({"successful":", ".join(successful)}), 200
        else:
            res = init_assistant.delay(orga.id)
            res.forget()
            return jsonify(), 200
    except Exception:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occured"}), 500
    
@api_bp.route("/me", methods=["GET"])
@login_required
def me():
    try:
        logo = current_user.organization.logo()
        data_url = None
        
        if logo is not None:
            encoded_logo = base64.urlsafe_b64encode(logo.data).decode("utf-8")
            mime_type, _ = mimetypes.guess_type(logo.filename)
            data_url = f'data:{mime_type};base64,{encoded_logo}'
            
        return jsonify({
            "name": current_user.name,
            "companyName": current_user.organization.name,
            "logoURL": data_url
        }), 200
    except:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occoured"}), 500

@api_bp.route("/update_all_entries", methods=["GET"])
@login_required
def update_all_entries():
    IGApiFetcher.updateAllEntries(current_user.oauth.token["access_token"], current_user)
    return jsonify({}), 200