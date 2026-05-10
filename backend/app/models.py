from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    race_results = db.relationship('RaceResult', backref='user', lazy=True)

class Passage(db.Model):
    __tablename__ = 'passages'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    length = db.Column(db.Integer)
    difficulty = db.Column(db.String(50))

    races = db.relationship('Race', backref='passage', lazy=True)


class Race(db.Model):
    __tablename__ = 'races'

    id = db.Column(db.Integer, primary_key=True)
    passage_id = db.Column(db.Integer, db.ForeignKey('passages.id'), nullable=False)
    race_type = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='waiting')
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    results = db.relationship('RaceResult', backref='race', lazy=True)


class RaceResult(db.Model):
    __tablename__ = 'race_results'

    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('races.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    wpm = db.Column(db.Integer)
    accuracy = db.Column(db.Float)
    place = db.Column(db.Integer)
    completed = db.Column(db.Boolean, default=False)