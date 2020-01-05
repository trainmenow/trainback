from datetime import datetime
from trainback import db, flask_bcrypt

class Account(db.Model):
    """ User Account Model for storing user related details """
    __tablename__ = "user_accounts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(255), unique=True)
    activated = db.Column(db.Boolean, nullable=False, default=False)
    blocked = db.Column(db.Boolean, nullable=False, default=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    pw_hash = db.Column(db.String(255))
    registered = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.pw_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.pw_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)


class Code(db.Model):
    """ User Code Model for verify email """
    __tablename__ = "user_codes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(255), unique=True, nullable=False)
    purpose = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)