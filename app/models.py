from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from datetime import datetime

followers = db.Table("followers",
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("following_id", db.Integer, db.ForeignKey("user.id"))
)


class User(UserMixin, db.Model):
    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username      = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email         = db.Column(db.String(64), index=True, unique=True)
    birthday      = db.Column(db.Date)
    description   = db.Column(db.String(128))
    gender        = db.Column(db.CHAR)
    last_seen     = db.Column(db.DateTime, default=datetime.utcnow())

    following = db.relationship(
        "User", secondary = followers,
        primaryjoin   = (followers.c.follower_id == id),
        secondaryjoin = (followers.c.following_id == id),
        backref       = db.backref("followers", lazy="dynamic"),
        lazy          = "dynamic"
    )

    def follow(self, user):
        if not self.is_following(user):
            self.following.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(followers.c.following_id == user.id).count() > 0


    messages_sent = db.relationship("Message",
        foreign_keys = "Message.sender_id",
        backref      = "author", lazy="dynamic"
    )

    messages_received = db.relationship("Message",
        foreign_keys = "Message.recipient_id",
        backref      = "recipient", lazy="dynamic"
    )

    last_message_read_time = db.Column(db.DateTime)

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(Message.timestamp > last_read_time).count() 


    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return "https://gravatar.com/avatar/{}?d=robohash&s={}".format(digest, size)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Message(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    sender_id    = db.Column(db.Integer, db.ForeignKey("user.id"))
    recipient_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    subject      = db.Column(db.String(32))
    body         = db.Column(db.String(128))
    timestamp    = db.Column(db.DateTime, index=True, default=datetime.utcnow)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))