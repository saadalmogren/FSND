from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "capstone"
database_path = "postgres://{}:{}@{}/{}".format(
    'postgres', 'admin', 'localhost:5432', database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String, nullable=False)
    release_date = db.Column(Date, nullable=False)
    roles = db.relationship('Actor', backref='movie',
                            lazy=True, cascade='all, delete')

    def __init__(self, title, release_date):
        self.question = question
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


class Actor(db.Model):
    __tablename__ = "actors"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String, nullable=False)
    age = db.Column(Integer, nullable=False)
    gender = db.Column(String, nullable=False)
    roles = db.relationship('Actor', backref='actor',
                            lazy=True, cascade='all, delete')
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


class Role(db.Model):
    name = db.Column(String, primary_key=True)
    movie_id = db.Column(Integer, db.ForeignKey('movies.id'), primary_key=True)
    actor_id = db.Column(Integer, db.ForeignKey('actors.id'), primary_key=True)
    def __init__(self, name, movie_id, actor_id):
        self.name = name
        self.movie_id = movie_id
        self.actor_id = actor_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'name': self.name,
            'movie_id': self.movie_id,
            'actor_id': self.actor_id
        }
