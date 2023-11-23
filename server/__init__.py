from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from decouple import config
from openai import OpenAI
from .models import db, User
from .utils.env import ENV_VARS, DEFAULT_USERS

EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"

CLIENT = OpenAI(api_key=ENV_VARS["OPENAI_API_KEY"])
def create_app() -> Flask:
    
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    
    app.config['SECRET_KEY'] = ENV_VARS["FLASK_SECRET_KEY"]

    uri = ENV_VARS["DATABASE_URL"]
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    db.init_app(app)

    with app.app_context():
        db.create_all()
        
        # Default Users aus den .env-Vars hinzufügen
        if User.query.count() == 0:
            for user in DEFAULT_USERS:
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
