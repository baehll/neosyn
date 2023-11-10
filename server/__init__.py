from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from decouple import config
from openai import OpenAI

db = SQLAlchemy()

EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"

CLIENT = OpenAI(api_key=config("OPENAI_API_KEY"))
def create_app() -> Flask:
    
    app = Flask(__name__)
    cors = CORS(app, supports_credentials=True)
    
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    uri = config("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    db.init_app(app)


    from .views import views
    from .api import api

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')

    # from .models import User, Animal, Message

    with app.app_context():
        db.create_all()

    return app    
