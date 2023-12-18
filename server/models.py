from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import time

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class UserToken(db.Model):
    __tablename__ = "usertokens"
    
    id = db.Column(db.Integer, primary_key=True)
    expiration = db.Column(db.Integer, nullable=True)
    client_token = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    platform = db.Column(db.String(50), nullable=False)
    #platform_id = db.Column(db.String(200), nullable=False)
    
    def set_data(self, exp, token, platform):
        self.expiration = exp
        self.client_token = token
        self.platform = platform
    
    def is_expired(self):
        now = int(time.time() * 1000)
        return (now > self.expiration)
    
class Page(db.Model):
    __tablename__ = "pages"
    
    id = db.Column(db.Integer, primary_key=True)
    usertoken_id = db.Column(db.Integer, db.ForeignKey("usertokens.id"))
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200), nullable=True)
    can_analyze = db.Column(db.Boolean)
    can_advertise = db.Column(db.Boolean)
    can_moderate = db.Column(db.Boolean)
    can_create_content = db.Column(db.Boolean)
    can_manage = db.Column(db.Boolean)
    
class Business_Account(db.Model):
    __tablename__ = "business_accounts"
    
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey("pages.id"))
    followers_count = db.Column(db.Integer)
    
class Media(db.Model):
    __tablename__ = "medias"
    
    id = db.Column(db.Integer, primary_key=True)
    bzacc_id = db.Column(db.Integer, db.ForeignKey("business_accounts.id"))
    media_url = db.Column(db.String(450), nullable=False)
    permalink = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    etag = db.Column(db.String(50), nullable=False)
    
class Comment(db.Model):
    __tablename__  = "comments"
    
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("comments.id"))
    media_id = db.Column(db.Integer, db.ForeignKey("medias.id"))
    sentiment = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, nullable=False)
    etag = db.Column(db.String(50), nullable=False)