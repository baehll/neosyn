from flask import Flask, session
from blinker import signal
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from decouple import config
from openai import OpenAI
from .web.models import db, User, login_manager, EarlyAccessKeys
from .utils.env_utils import EnvManager 
from flask_migrate import Migrate
from flask_talisman import Talisman
from datetime import timedelta
import os

ENV = EnvManager()

gptConfig = {
    "EMBEDDING_MODEL":"text-embedding-ada-002", 
    "GPT_MODEL":"gpt-4-turbo-preview", 
    "CLIENT":OpenAI(api_key=config("OPENAI_API_KEY"))
}

def chatGPTModel():
    return gptConfig

def create_app() -> Flask:
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = config("FLASK_SECRET_KEY")
    app.config['FACEBOOK_OAUTH_CLIENT_ID'] = config("FACEBOOK_OAUTH_CLIENT_ID")
    app.config["FACEBOOK_OAUTH_CLIENT_SECRET"] = config("FACEBOOK_OAUTH_CLIENT_SECRET")
    
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=31)
    app.config["MAX_FILE_SIZE"] = 8 * 64 * 1024 * 1024 # 8 Dateien mit jeweils 64MB = 512 MB
    
    CORS(app)
    csp = {
        'default-src': [
            '\'self\'', 
            '*.quiet-mountain-69143-51eb8184b186.herokuapp.com', 
            'quiet-mountain-69143-51eb8184b186.herokuapp.com'
            ],
        'img-src': '*',
        'script-src': [
            '\'self\'',
            '\'unsafe-eval\''
            ],
        'style-src': [
            '\'self\'',
            '\'unsafe-inline\''
        ]        
    }
    
    if app.debug == True:
        csp["default-src"].append("https://localhost:5000")
        csp["default-src"].append("http://localhost:5000")
        
    Talisman(app, content_security_policy=csp)
    app.config["UPLOAD_FOLDER"] = config("COMPANY_FILE_UPLOAD_FOLDER")
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
        print(f"Upload Folder created under {app.config['UPLOAD_FOLDER']}")
        
    uri = config("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    
    db.init_app(app)
    login_manager.init_app(app)
    # Migration Script for DB
    migrate = Migrate(app, db)
    
    with app.app_context():
        db.create_all()
        
        if EarlyAccessKeys.query.count() == 0:
            key_string = config("EARLY_ACCESS_KEYS")
            if key_string != "":
                for k in key_string.split("//"):
                    ea_key = EarlyAccessKeys()
                    ea_key.set_key(k)
                    db.session.add(ea_key)
                db.session.commit()
                print("Early Access Keys zur DB hinzugefügt")
            else:
                print("Keine Early Access Keys in ENV oder DB gefunden")
    from .web.views import views
    from .web.api import api
    from .web.auth import authenticate

    #from .web.test import test
    #app.register_blueprint(test, url_prefix="/test")
    @app.before_request
    def setup():
        session.permanent = True
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(authenticate, url_prefix='/auth')

    return app    
