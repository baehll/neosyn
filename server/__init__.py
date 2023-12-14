from flask import Flask
from blinker import signal
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from decouple import config
from openai import OpenAI
from .models import db, User
from .utils.env_utils import EnvManager 
from flask_jwt_extended import JWTManager

EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"
JWT_REVOKED_TOKENS = set()

ENV = EnvManager()

CLIENT = OpenAI(api_key=config("OPENAI_API_KEY"))
user_logged_out = signal('user-logged-out')

def handle_user_logout(sender, **extra):
    jti = extra['jwt_payload']['jti']
    JWT_REVOKED_TOKENS.add(jti)

def check_jwt_token(*sender, **extra):
    jti = sender[1]['jti']
    if jti in JWT_REVOKED_TOKENS:
        return True
    return False

def create_app() -> Flask:
    
    app = Flask(__name__)

    app.config['SECRET_KEY'] = config("FLASK_SECRET_KEY")
    app.config['JWT_SECRET_KEY'] = config("JWT_SECRET_TOKEN")
    app.config['JWT_IDENTITY_CLAIM'] = 'sub'

    CORS(app, supports_credentials=True)
    jwt = JWTManager(app)

    jwt.token_in_blocklist_loader(check_jwt_token)

    user_logged_out.connect(handle_user_logout, app)

    uri = config("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    db.init_app(app)

    with app.app_context():
        db.create_all()
        
        # Default Users aus den .env-Vars hinzufügen, wenn die DB 
        if User.query.count() == 0:
            ENV.init_default_users()
            for user in ENV.DEFAULT_USERS:
                u = User(username=user[0])
                u.set_password(user[1])
                db.session.add(u)
            db.session.commit()
            print("Default Users aus ENV_VAR hinzugefügt")

    from .views import views
    from .api import api
    from .authenticate import authenticate

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(authenticate, url_prefix='/auth')

    return app    
