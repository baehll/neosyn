from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from decouple import config


db = SQLAlchemy()

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

    app.register_blueprint(views, url_prefix='/')


    # from .models import User, Animal, Message

    with app.app_context():
        db.create_all()

    return app    
