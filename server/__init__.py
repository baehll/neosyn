from flask import Flask, session
from blinker import signal
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from decouple import config
from openai import OpenAI
from .web.models import db, User, login_manager, EarlyAccessKeys, Platform, _PlatformEnum
from .utils.env_utils import EnvManager 
from flask_migrate import Migrate
from flask_talisman import Talisman
from datetime import timedelta
import os

ENV = EnvManager()

class GPTConfig():
    EMBEDDING_MODEL="text-embedding-ada-002" 
    GPT_MODEL="gpt-4-turbo"
    CLIENT=OpenAI(api_key=config("OPENAI_API_KEY"))


def create_app() -> Flask:
    app = Flask(__name__)
    
    app.config["CONFIG_FOLDER"] = config("CONFIG_FOLDER")
    app.config["GPT_ASSISTANT_ID"] = config("GPT_ASSISTANT_ID")
    
    app.config['SECRET_KEY'] = config("FLASK_SECRET_KEY")
    app.config['FACEBOOK_OAUTH_CLIENT_ID'] = config("FACEBOOK_OAUTH_CLIENT_ID")
    app.config["FACEBOOK_OAUTH_CLIENT_SECRET"] = config("FACEBOOK_OAUTH_CLIENT_SECRET")
    
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=31)
    app.config["MAX_FILE_SIZE"] = 8 * 64 * 1024 * 1024 # 8 Dateien mit jeweils 64MB = 512 MB

    cors_domains = ["https://unaite.ai", "http://unaite.ai", "https://quiet-mountain-69143-51eb8184b186.herokuapp.com", "http://quiet-mountain-69143-51eb8184b186.herokuapp.com"]
    CORS(app,
        origins=cors_domains,
        resources={
            r"/*": {"origins": cors_domains}},
        supports_credentials=True
    )

    csp = {
        'default-src': [
            '\'self\'', 
            '*.quiet-mountain-69143-51eb8184b186.herokuapp.com', 
            'quiet-mountain-69143-51eb8184b186.herokuapp.com'
            ],
        'img-src':  [
            '\'self\'',
            'data:'
            ],
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
                print("Keine Early Access Keys in ENV gefunden")
        
        if Platform.query.count() == 0:
            platform_string = config("IMPLEMENTED_PLATFORMS")
            implemented_platforms = []
            if platform_string != "":
                for p in platform_string.split("//"):
                    implemented_platforms.append(_PlatformEnum[p])
                    p_db = Platform(name=_PlatformEnum[p], is_implemented=True)
                    db.session.add(p_db)
            else: 
                print("Keine implementierten Plattformen gefunden")
            for p_e in _PlatformEnum:
                if p_e not in implemented_platforms:
                    db.session.add(Platform(name=p_e.name, is_implemented=False))
            db.session.commit()
            
    from .web.views import views
    from .web.api import api_bp
    from .web.api.data import threads_bp
    from .web.api.ai import ai_bp
    from .web.auth import authenticate

    @app.before_request
    def setup():
        session.permanent = True
    
    app.register_blueprint(views, url_prefix='/')
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(threads_bp, url_prefix="/api/data/threads")
    app.register_blueprint(ai_bp, url_prefix="/api/data/ai")
    
    app.register_blueprint(authenticate, url_prefix='/auth')

    if app.debug == True:
        from .web.test import test
        app.register_blueprint(test, url_prefix="/test")
        
    return app    
