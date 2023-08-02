"""Models for authen. author. app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


# class Feedback(db.Model):
#     __tablename__ = 'feedbacks'


# class User(db.Model):

#     __tablename__ = 'users'
