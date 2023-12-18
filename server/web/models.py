from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import time

db = SQLAlchemy()

class _IGBaseTable(db.Model):
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    etag = db.Column(db.String(50), nullable=False)

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    usertokens = db.relationship("UserToken", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class UserToken(db.Model):
    __tablename__ = "usertokens"
    
    id = db.Column(db.Integer, primary_key=True)
    expiration = db.Column(db.Integer, nullable=True)
    client_token = db.Column(db.String(200), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="usertokens")
    
    pages = db.relationship('Pages', back_populates='usertoken')

    
    def set_data(self, exp, token, platform):
        self.expiration = exp
        self.client_token = token
        self.platform = platform
    
    def is_expired(self):
        now = int(time.time() * 1000)
        return (now > self.expiration)

class Page(_IGBaseTable):
    __tablename__ = "pages"
    
    usertoken_id = db.Column(db.Integer, db.ForeignKey("usertokens.id"))
    usertoken = db.relationship('UserToken', back_populates='pages')

    business_accounts = db.relationship("Business_Account", back_populates="page")

    fb_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200), nullable=True)
    can_analyze = db.Column(db.Boolean, default=False)
    can_advertise = db.Column(db.Boolean, default=False)
    can_moderate = db.Column(db.Boolean, default=False)
    can_message = db.Column(db.Boolean, default=False)
    can_create_content = db.Column(db.Boolean, default=False)
    can_manage = db.Column(db.Boolean, default=False)
    
    def setTasks(self, analyze=False, advertise=False, moderate=False, message=False, create_content=False, manage=False):
        self.can_analyze = analyze
        self.can_advertise = advertise
        self.can_moderate = moderate
        self.can_message = message
        self.can_create_content = create_content
        self.can_manage = manage
    
class Business_Account(_IGBaseTable):
    __tablename__ = "business_accounts"
    
    page = db.relationship("Page", back_populates="business_accounts")
    page_id = db.Column(db.Integer, db.ForeignKey("pages.id"))
    
    fb_id = db.Column(db.Integer, nullable=False)
    followers_count = db.Column(db.Integer)
    
    medias = db.relationship("Media", back_populates="bzacc")
    
class Media(_IGBaseTable):
    __tablename__ = "medias"
    
    bzacc_id = db.Column(db.Integer, db.ForeignKey("business_accounts.id"))
    bzacc = db.relationship("Business_Account", back_populates="medias")
    
    fb_id = db.Column(db.Integer, nullable=False)
    media_url = db.Column(db.String(450), nullable=False)
    permalink = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    
    comments = db.relationship("Comment", back_populates="media")
    
class Comment(_IGBaseTable):
    __tablename__  = "comments"
    
    parent_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=True)
    children = db.relationship("Comment")
    
    media_id = db.Column(db.Integer, db.ForeignKey("medias.id"))
    media = db.relationship("Media", back_populates="comments")
    
    fb_id = db.Column(db.Integer, nullable=False)
    sentiment = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, nullable=False)