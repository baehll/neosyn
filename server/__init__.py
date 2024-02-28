from flask import Flask
from blinker import signal
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from decouple import config
from openai import OpenAI
from .web.models import db, User, login_manager
from .utils.env_utils import EnvManager 
from flask_migrate import Migrate

ENV = EnvManager()

gptConfig = {
    "EMBEDDING_MODEL":"text-embedding-ada-002", 
    "GPT_MODEL":"gpt-3.5-turbo", 
    "CLIENT":OpenAI(api_key=config("OPENAI_API_KEY"))
}

def chatGPTModel():
    return gptConfig

def create_app() -> Flask:
    
    app = Flask(__name__)

    app.config['SECRET_KEY'] = config("FLASK_SECRET_KEY")
    app.config['FACEBOOK_OAUTH_CLIENT_ID'] = config("FACEBOOK_OAUTH_CLIENT_ID")
    app.config["FACEBOOK_OAUTH_CLIENT_SECRET"] = config("FACEBOOK_OAUTH_CLIENT_SECRET")
    CORS(app, supports_credentials=True)

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

    from .web.views import views
    from .web.api import api
    from .web.auth import authenticate

    #from .web.test import test
    #app.register_blueprint(test, url_prefix="/test")
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(authenticate, url_prefix='/auth')

    return app    
