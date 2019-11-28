# pylint: disable=E1101
from datetime import datetime
from trainback import db, flask_bcrypt

class Account(db.Model):
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