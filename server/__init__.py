from flask import Flask
from blinker import signal
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from decouple import config
from openai import OpenAI
from .web.models import db, User
from .utils.env_utils import EnvManager 
from flask_migrate import Migrate

gptConfig = {
    "EMBEDDING_MODEL":"text-embedding-ada-002", 
    "GPT_MODEL":"gpt-3.5-turbo", 
    "CLIENT":OpenAI(api_key=config("OPENAI_API_KEY"))
}

def chatGPTModel():
    return gptConfig

ENV = EnvManager()

def create_app() -> Flask:
    
    app = Flask(__name__)

    app.config['SECRET_KEY'] = config("FLASK_SECRET_KEY")
    app.config['JWT_SECRET_KEY'] = config("JWT_SECRET_TOKEN")
    app.config['JWT_IDENTITY_CLAIM'] = 'sub'

    CORS(app, supports_credentials=True)

    uri = config("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    db.init_app(app)
    
    # Migration Script for DB
    migrate = Migrate(app, db)
    
    with app.app_context():
        db.create_all()
        
        # Default Users aus den .env-Vars hinzufügen, wenn die DB leer ist
        if User.query.count() == 0:
            ENV.init_default_users()
            for user in ENV.DEFAULT_USERS:
                u = User(username=user[0])
                u.set_password(user[1])
                db.session.add(u)
            db.session.commit()
            print("Default Users aus ENV_VAR hinzugefügt")

    from .web.views import views
    from .web.api import api
    from .web.authenticate import authenticate

    #from .web.test import test
    #app.register_blueprint(test, url_prefix="/test")
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(authenticate, url_prefix='/auth')

    return app    
