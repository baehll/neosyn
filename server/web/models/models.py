from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from flask_login import LoginManager, UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from enum import Enum, auto
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class _PlatformEnum(Enum):
    Meta = auto()

class _Base(db.Model):
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True) 
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class _IGBaseTable(_Base):
    __abstract__ = True
    
    etag = db.Column(db.String(50), nullable=True)
    fb_id = db.Column(db.Integer, nullable=False)

class EarlyAccessKeys(_Base):
    hashed_key = db.Column(db.String(200), nullable=False)

    def set_key(self, key):
        self.hashed_key = generate_password_hash(key)
    
    def check_key(self, key):
        return check_password_hash(self.hashed_key, key)

class Organization(_Base):
    __tablename__ = "organizations"
    name = db.Column(db.String(256))
    users = db.relationship("User", back_populates="")

    assistant_id = db.Column(db.String(256))
    folder_path = db.Column(db.String(256), unique=True)
    logo_file = db.Column(db.String(256))

class User(_Base, UserMixin):
    __tablename__ = "users"
    
    orga_id = db.Column(db.Integer, db.ForeignKey("organizations.id"))
    organization = db.relationship("Organization", back_populates="users")
    
    name = db.Column(db.String(256))
    pages = db.relationship("IGPage", back_populates="user")
    platform = db.Column(db.Enum(_PlatformEnum))
    
class OAuth(OAuthConsumerMixin, _Base):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)

class IGPage(_IGBaseTable):
    __tablename__ = "ig_pages"
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship('User', back_populates='pages')

    business_accounts = db.relationship("IGBusinessAccount", back_populates="page")

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
    
class IGBusinessAccount(_IGBaseTable):
    __tablename__ = "ig_business_accounts"
    
    page_id = db.Column(db.Integer, db.ForeignKey("ig_pages.id"))
    page = db.relationship("IGPage", back_populates="business_accounts")
    
    followers_count = db.Column(db.Integer)
    
    medias = db.relationship("IGMedia", back_populates="bzacc")

class IGInteraction(db.Model):
    __tablename__ = "ig_interactions"
    
    media_id = db.Column(db.ForeignKey("ig_medias.id"), primary_key=True)
    comment_id = db.Column(db.ForeignKey("ig_comments.id"), primary_key=True)
    customer_id = db.Column(db.ForeignKey("ig_customers.id"), primary_key=True)
    
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    
    media = db.relationship("IGMedia", back_populates="interaction_association")
    customer = db.relationship("IGCustomer", back_populates="interaction_association")
    comment = db.relationship("IGComment", back_populates="interaction_association")
    
class IGMedia(_IGBaseTable):
    __tablename__ = "ig_medias"
    
    bzacc_id = db.Column(db.Integer, db.ForeignKey("ig_business_accounts.id"))
    bzacc = db.relationship("IGBusinessAccount", back_populates="medias")
    
    media_url = db.Column(db.String(450), nullable=False)
    permalink = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    
    interaction_association = db.relationship("IGInteraction", back_populates="media")
    customers = association_proxy("interaction_association", "customer")
    comments = association_proxy("interaction_association", "comment")
    
class IGCustomer(_IGBaseTable):
    __tablename__ = "ig_customers"

    name = db.Column(db.String(200), nullable=False)
    
    interaction_association = db.relationship("IGInteraction", back_populates="customer")
    medias = association_proxy("interaction_association", "media")
    comments = association_proxy("interaction_association", "comment")
    
class IGComment(_IGBaseTable):
    __tablename__  = "ig_comments"
    
    parent_id = db.Column(db.Integer, db.ForeignKey("ig_comments.id"), nullable=True)
    children = db.relationship("IGComment")
    
    interaction_association = db.relationship("IGInteraction", back_populates="comment")
    
    customers = association_proxy("interaction_association", "customer")
    medias = association_proxy("interaction_association", "media")
    
    sentiment = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, nullable=False)


login_manager = LoginManager()
login_manager.login_view = "facebook.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))