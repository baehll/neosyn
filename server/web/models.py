from flask_sqlalchemy import SQLAlchemy
import time
from enum import Enum, auto

db = SQLAlchemy()

class _PlatformEnum(Enum):
    IG = auto()
    FB = auto()

class _Base(db.Model):
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True) 
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class _IGBaseTable(_Base):
    __abstract__ = True
    
    etag = db.Column(db.String(50), nullable=True)
    fb_id = db.Column(db.Integer, nullable=False)

class User(_Base):
    __tablename__ = "users"
    
    usertokens = db.relationship("UserToken", back_populates="user")
    
class UserToken(_Base):
    __tablename__ = "usertokens"
    
    expiration = db.Column(db.Integer, nullable=True)
    client_token = db.Column(db.String(200), nullable=False)
    platform = db.Column(db.Enum(_PlatformEnum), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="usertokens")
    
    pages = db.relationship('Page', back_populates='usertokens')
    
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
    usertokens = db.relationship('UserToken', back_populates='pages')

    business_accounts = db.relationship("BusinessAccount", back_populates="page")

    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200), nullable=True)
    can_analyze = db.Column(db.Boolean, default=False)
    can_advertise = db.Column(db.Boolean, default=False)
    can_moderate = db.Column(db.Boolean, default=False)
    can_message = db.Column(db.Boolean, default=False)
    can_create_content = db.Column(db.Boolean, default=False)
    can_manage = db.Column(db.Boolean, default=False)
    followers_count = db.Column(db.Integer, nullable=True)
    
    def setTasks(self, analyze=False, advertise=False, moderate=False, message=False, create_content=False, manage=False):
        self.can_analyze = analyze
        self.can_advertise = advertise
        self.can_moderate = moderate
        self.can_message = message
        self.can_create_content = create_content
        self.can_manage = manage
    
class BusinessAccount(_IGBaseTable):
    __tablename__ = "business_accounts"
    
    page_id = db.Column(db.Integer, db.ForeignKey("pages.id"))
    page = db.relationship("Page", back_populates="business_accounts")
    
    followers_count = db.Column(db.Integer)
    
    medias = db.relationship("Media", back_populates="bzacc")
    
class Media(_IGBaseTable):
    __tablename__ = "medias"
    
    bzacc_id = db.Column(db.Integer, db.ForeignKey("business_accounts.id"))
    bzacc = db.relationship("BusinessAccount", back_populates="medias")
    
    media_url = db.Column(db.String(450), nullable=False)
    permalink = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    
    comments = db.relationship("Comment", back_populates="media")
    
class Comment(_IGBaseTable):
    __tablename__  = "comments"
    
    from_user = db.Column(db.Integer, nullable=False)
    
    parent_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=True)
    children = db.relationship("Comment")
    
    media_id = db.Column(db.Integer, db.ForeignKey("medias.id"))
    media = db.relationship("Media", back_populates="comments")
    
    sentiment = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, nullable=False)