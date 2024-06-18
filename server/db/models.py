from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from flask_login import LoginManager, UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from enum import Enum, auto
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timezone, datetime

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
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __str__(self):
        return "<" + self.__class__.__name__ + " " + str(self.id) + " " +  str(self.to_dict()) + ">"

class _IGBaseTable(_Base):
    __abstract__ = True
    
    etag = db.Column(db.String, nullable=True)
    fb_id = db.Column(db.String, nullable=False, unique=True)

class Platform(_Base):
    __tablename__ = "platforms"
    
    name = db.Column(db.Enum(_PlatformEnum))
    is_implemented = db.Column(db.Boolean, default=False)
    icon = db.Column(db.String)

class EarlyAccessKeys(_Base):
    hashed_key = db.Column(db.String, nullable=False)

    def set_key(self, key):
        self.hashed_key = generate_password_hash(key)
    
    def check_key(self, key):
        return check_password_hash(self.hashed_key, key)

class File(_Base):
    __tablename__ = "files"
    
    orga_id = db.Column(db.Integer, db.ForeignKey("organizations.id"))
    organization = db.relationship("Organization", back_populates="files", foreign_keys=[orga_id])
    
    data = db.Column(db.LargeBinary)
    filename = db.Column(db.String)

class Organization(_Base):
    __tablename__ = "organizations"
    name = db.Column(db.String)
    
    users = db.relationship("User", back_populates="organization")
    generated_runs = db.relationship("OpenAIRun", back_populates="organization")
    interaction_examples = db.relationship("InteractionExamples", back_populates="organization")
    
    files = db.relationship("File", back_populates="organization", foreign_keys=[File.orga_id])
    
    vec_storage_id = db.Column(db.String)

    logo_id = db.Column(db.Integer)
    logo = db.relationship("File", back_populates="organization", uselist=False, overlaps="files")

    def logo(self):
        return File.query.filter_by(id=self.logo_id).first()

class InteractionExamples(_Base):
    __tablename__ = "interaction_examples"
    
    orga_id = db.Column(db.Integer, db.ForeignKey("organizations.id"))
    organization = db.relationship("Organization", back_populates="interaction_examples")
    
    user_msg = db.Column(db.String)
    customer_msg = db.Column(db.String)
    
    def export(self):
        return "{'customer': '" + self.customer_msg + "', 'user': '" + self.user_msg + "'}"

class OpenAIRun(_Base):
    __tablename__ = "openai_runs"
    run_id = db.Column(db.String)
    
    orga_id = db.Column(db.Integer, db.ForeignKey("organizations.id"))
    organization = db.relationship("Organization", back_populates="generated_runs")

class User(_Base, UserMixin):
    __tablename__ = "users"
    
    orga_id = db.Column(db.Integer, db.ForeignKey("organizations.id"))
    organization = db.relationship("Organization", back_populates="users")
    
    name = db.Column(db.String)
    pages = db.relationship("IGPage", back_populates="user")

    platform_id = db.Column(db.Integer, db.ForeignKey("platforms.id"))
    platform = db.relationship("Platform")
    
    answer_improvements = db.relationship("AnswerImprovements", back_populates="user")    
    oauth = db.relationship("OAuth", back_populates="user", uselist=False)
    
class OAuth(OAuthConsumerMixin, _Base):
    provider_user_id = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship("User", back_populates="oauth")

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
    
    name = db.Column(db.String)
    profile_picture_url = db.Column(db.String)    
    
    medias = db.relationship("IGMedia", back_populates="bzacc")
    # threads = db.relationship("IGThread", back_populates="bzacc")
    
    # customer_id = db.Column(db.Integer, db.ForeignKey("ig_customers.id"))
    # customer = db.relationship("IGCustomer", back_populates="bz_acc")

# class IGThread(_Base):
#     __tablename__ = "ig_threads"
    
#     media_id = db.Column(db.ForeignKey("ig_medias.id"))
#     customer_id = db.Column(db.ForeignKey("ig_customers.id"))
#     bzacc_id = db.Column(db.ForeignKey("ig_business_accounts.id"))
    
#     is_unread = db.Column(db.Boolean, nullable=False, default=True)
#     is_bookmarked = db.Column(db.Boolean, default=False)
    
#     media = db.relationship("IGMedia", back_populates="thread_association")
#     customer = db.relationship("IGCustomer", back_populates="thread_association")
#     bzacc = db.relationship("IGBusinessAccount", back_populates="threads")
    
#     comments = db.relationship("IGComment", back_populates="thread")
    
#     answer_improvements = db.relationship("AnswerImprovements", back_populates="thread")
    
class IGMedia(_IGBaseTable):
    __tablename__ = "ig_medias"
    
    bzacc_id = db.Column(db.Integer, db.ForeignKey("ig_business_accounts.id"))
    bzacc = db.relationship("IGBusinessAccount", back_populates="medias")
    
    media_url = db.Column(db.String, nullable=False)
    permalink = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    like_count = db.Column(db.Integer, nullable=False, default=0)
    comments_count = db.Column(db.Integer, nullable=False, default=0)
    media_type = db.Column(db.String, nullable=False)
    
    caption = db.Column(db.String)
    
    gpt_thread_id = db.Column(db.String)
    
    oldest_comment_timestamp = db.Column(db.DateTime)
    latest_comment_timestamp = db.Column(db.DateTime)
    
    answer_improvements = db.relationship("AnswerImprovements", back_populates="media")
    #thread_association = db.relationship("IGThread", back_populates="media")
    #customers = association_proxy("thread_association", "customer")
    
    #comments = db.relationship("IGComment", back_populates="media")
    
# class IGCustomer(_IGBaseTable):
#     __tablename__ = "ig_customers"

#     name = db.Column(db.String, nullable=False)
#     profile_picture_url = db.Column(db.String)    
    
#     thread_association = db.relationship("IGThread", back_populates="customer")
#     medias = association_proxy("thread_association", "media")
    
#     comments = db.relationship("IGComment", back_populates="customer")
#     bz_acc = db.relationship("IGBusinessAccount", back_populates="customer")
    
# class IGComment(_IGBaseTable):
#     __tablename__  = "ig_comments"
    
#     parent_id = db.Column(db.Integer, db.ForeignKey("ig_comments.id"), nullable=True)
#     parent = db.relationship("IGComment", remote_side="IGComment.id",backref="children")
    
#     thread_id = db.Column(db.Integer, db.ForeignKey("ig_threads.id"))
#     thread = db.relationship("IGThread", back_populates="comments")
    
#     media_id = db.Column(db.Integer, db.ForeignKey("ig_medias.id"))
#     media = db.relationship("IGMedia", back_populates="comments")
    
#     customer_id = db.Column(db.Integer, db.ForeignKey("ig_customers.id"))
#     customer = db.relationship("IGCustomer", back_populates="comments")
    
#     sentiment = db.Column(db.Integer)
#     timestamp = db.Column(db.DateTime, nullable=False)

#     text = db.Column(db.String)
#     like_count = db.Column(db.Integer, default=0)

class AnswerImprovements(_Base):
    __tablename__ = "answer_improvements"
    
    generated_answer = db.Column(db.String)
    improved_answer = db.Column(db.String)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="answer_improvements")
    
    ig_media = db.Column(db.Integer, db.ForeignKey("ig_medias.id"))
    media = db.relationship("IGMedia", back_populates="answer_improvements")
    
login_manager = LoginManager()
login_manager.login_view = "facebook.login"

@login_manager.user_loader
def load_user(user_id):
    #print(User.query.get(int(user_id)))
    return User.query.filter(User.id == int(user_id)).first()
