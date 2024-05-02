from flask import (
    Blueprint, jsonify, request, session, current_app
)
import os
import requests
from flask_login import login_required, current_user
from decouple import config
from ..models import db, User , _PlatformEnum, Organization, OAuth, Platform
from pathvalidate import replace_symbol
from ...utils import file_utils, IGApiFetcher
from werkzeug.utils import secure_filename
import traceback

api_bp = Blueprint('api', __name__)

def GPTModel():
    from server import chatGPTModel
    return chatGPTModel()

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
            if len(errors) > 0:
                return jsonify({"error": errors, "successful":", ".join(successful) }), 422
            else:
                return jsonify({"successful":", ".join(successful)}), 200
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error":"An exception has occoured"}), 500
    return jsonify({}), 200

@api_bp.route("/update_interactions", methods=["GET"])
@login_required
def update_interactions():
    # try:
    #     # access token aus DB nehmen
    #     oauth = db.session.execute(db.select(OAuth).filter(OAuth.user.has(id=current_user.id))).scalar_one_or_none()
    #     IGApiFetcher.update_all_entries(oauth.token["access_token"], current_user)
    #     return jsonify({}), 200
    # except Exception as e:
    #     print(e)
    #     return jsonify({"error":"An exception has occoured"}), 500
    oauth = db.session.execute(db.select(OAuth).filter(OAuth.user.has(id=current_user.id))).scalar_one_or_none()
    IGApiFetcher.update_all_entries(oauth.token["access_token"], current_user)
    return jsonify({}), 200
        

@api_bp.route("/fast_response", methods=["POST"])
@login_required
def fast_response():
    print(request.get_json())
    comment = request.get_json()["comment"]
    prompt = f'''
        Generiere 5 Antworten auf das folgende Kommentar, als wärst du ein Social Media Manager für ein Unternehmen.
        Antworte ausschließlich in Form eines Arrays, in dem die einzelnen Antworten Elemente des Arrays darstellen. 
        Das Array soll so strukturiert sein, dass es von Javascript als Array erkannt wird.
        user: {comment}
        bot:
    '''
    response = GPTModel()["CLIENT"].chat.completions.create(
        model = GPTModel()["GPT_MODEL"],
        messages=[{'role': 'user', 'content': prompt}]
    )
    output = response.choices[0].message.content.split("\"")[1::2]
    print(output)
    return jsonify({"answers": output})

@api_bp.route("/context_response", methods=["POST"])
@login_required
def context_response():
    comment_line = ""
    if(request.get_json()["comment"] != ""):
        comment_line = f'Kommentar: {request.get_json()["comment"]}'

    prompt = f'''
        Generiere eine Antwort auf folgenden Social Media Beitrag:
        Bild URL: {request.get_json()["media_url"]}
        Beitrag: {request.get_json()["caption"]}
    '''

    prompt = prompt + comment_line + '''
        Deine Antwort soll sich auf das Bild in der URL, den Beitrag sowie das Kommentar (falls vorhanden) beziehen.
        Antworte mit einem unformatierten String 
    '''

    response = GPTModel()["CLIENT"].chat.completions.create(
        model = GPTModel()["GPT_MODEL"],
        messages=[{'role': 'user', 'content': prompt}]
    )

    return jsonify({"answer": response.choices[0].message.content})
