from datetime import datetime
from trainback import db, flask_bcrypt

class Workout(db.Model):
    """ Workout Model for storing workout related details """
    __bind_key__ = 'trainlog'
    __tablename__ = "workouts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, default='new workout')
    owner = db.Column(db.String(255), nullable=False)
    note = db.Column(db.Text)
    length = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return "<Workout '{}'>".format(self.name)

    
class Segment(db.Model):
    """ Segment Model for storing workout related details """
    __bind_key__ = 'trainlog'
    __tablename__ = "segments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pos = db.Column(db.Integer, nullable=False)
    pause = db.Column(db.Integer, nullable=False, default=0)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)


class TrainingSet(db.Model):
    """ Set Model for storing workout related details """
    __bind_key__ = 'trainlog'
    __tablename__ = "training_set"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pos = db.Column(db.Integer, nullable=False)
    repeats = db.Column(db.Integer, nullable=False)
    weights = db.Column(db.Float, nullable=False)
    pause = db.Column(db.Integer, nullable=False, default=0)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)


class Exercise(db.Model):   
    """ Exercise Model for storing exercise related details """
    __bind_key__ = 'trainlog'
    __tablename__ = "exercise"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    inter_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    equipment = db.Column(db.String(255), nullable=False, default='')
    group = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)