from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from flask_login import LoginManager, UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from enum import Enum, auto
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class _PlatformEnum(Enum):
    Instagram = auto()
    TikTok = auto()
    YouTube = auto()
    Whatsapp = auto()
    LinkedIn = auto()
    X = auto()

class _Base(db.Model):
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True) 
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __str__(self):
        return "<" + self.__class__.__name__ + " " + str(self.id) + " " +  str(self.to_dict()) + ">"

class _IGBaseTable(_Base):
    __abstract__ = True
    
    etag = db.Column(db.String, nullable=True)
    fb_id = db.Column(db.String, nullable=False)

class Platform(_Base):
    __tablename__ = "platforms"
    
    name = db.Column(db.Enum(_PlatformEnum))
    is_implemented = db.Column(db.String, default=False)

class EarlyAccessKeys(_Base):
    hashed_key = db.Column(db.String, nullable=False)

    def set_key(self, key):
        self.hashed_key = generate_password_hash(key)
    
    def check_key(self, key):
        return check_password_hash(self.hashed_key, key)

class Organization(_Base):
    __tablename__ = "organizations"
    name = db.Column(db.String)
    users = db.relationship("User", back_populates="")

    assistant_id = db.Column(db.String)
    folder_path = db.Column(db.String, unique=True)
    logo_file = db.Column(db.String)

class User(_Base, UserMixin):
    __tablename__ = "users"
    
    orga_id = db.Column(db.Integer, db.ForeignKey("organizations.id"))
    organization = db.relationship("Organization", back_populates="users")
    
    name = db.Column(db.String)
    pages = db.relationship("IGPage", back_populates="user")
    platform_id = db.Column(db.Integer, db.ForeignKey("platforms.id"))
    platform = db.relationship("Platform")
    
class OAuth(OAuthConsumerMixin, _Base):
    provider_user_id = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)

class IGPage(_IGBaseTable):
    __tablename__ = "ig_pages"
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship('User', back_populates='pages')

    business_accounts = db.relationship("IGBusinessAccount", back_populates="page")

    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=True)
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
    
class IGBusinessAccount(_IGBaseTable):
    __tablename__ = "ig_business_accounts"
    
    page_id = db.Column(db.Integer, db.ForeignKey("ig_pages.id"))
    page = db.relationship("IGPage", back_populates="business_accounts")
    
    followers_count = db.Column(db.Integer)
    
    medias = db.relationship("IGMedia", back_populates="bzacc")

class IGThread(_Base):
    __tablename__ = "ig_threads"
    
    media_id = db.Column(db.ForeignKey("ig_medias.id"))
    customer_id = db.Column(db.ForeignKey("ig_customers.id"))
    
    is_unread = db.Column(db.Boolean, nullable=False, default=True)
    
    media = db.relationship("IGMedia", back_populates="thread_association")
    customer = db.relationship("IGCustomer", back_populates="thread_association")
    
    comments = db.relationship("IGComment", back_populates="thread")
    
class IGMedia(_IGBaseTable):
    __tablename__ = "ig_medias"
    
    bzacc_id = db.Column(db.Integer, db.ForeignKey("ig_business_accounts.id"))
    bzacc = db.relationship("IGBusinessAccount", back_populates="medias")
    
    media_url = db.Column(db.String, nullable=False)
    permalink = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    like_count = db.Column(db.Integer, nullable=False, default=0)
    comments_count = db.Column(db.Integer, nullable=False, default=0)
    
    caption = db.Column(db.String)
    
    thread_association = db.relationship("IGThread", back_populates="media")
    customers = association_proxy("thread_association", "customer")
    
    comments = db.relationship("IGComment", back_populates="media")
    
class IGCustomer(_IGBaseTable):
    __tablename__ = "ig_customers"

    name = db.Column(db.String, nullable=False)
    profile_picture_url = db.Column(db.String)    
    
    thread_association = db.relationship("IGThread", back_populates="customer")
    medias = association_proxy("thread_association", "media")
    
    comments = db.relationship("IGComment", back_populates="customer")
    
class IGComment(_IGBaseTable):
    __tablename__  = "ig_comments"
    
    parent_id = db.Column(db.Integer, db.ForeignKey("ig_comments.id"), nullable=True)
    parent = db.relationship("IGComment", remote_side="IGComment.id",backref="children")
    
    thread_id = db.Column(db.Integer, db.ForeignKey("ig_threads.id"))
    thread = db.relationship("IGThread", back_populates="comments")
    
    media_id = db.Column(db.Integer, db.ForeignKey("ig_medias.id"))
    media = db.relationship("IGMedia", back_populates="comments")
    
    customer_id = db.Column(db.Integer, db.ForeignKey("ig_customers.id"))
    customer = db.relationship("IGCustomer", back_populates="comments")
    
    sentiment = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, nullable=False)

    text = db.Column(db.String)

login_manager = LoginManager()
login_manager.login_view = "facebook.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))