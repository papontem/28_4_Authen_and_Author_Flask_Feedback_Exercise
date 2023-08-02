"""Models for authen. author. app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

# Part 1: Create User Model
class User(db.Model):

    __tablename__ = 'users'

    username   = db.Column(db.String(20), primary_key=True)
    password   = db.Column(db.String, nullable=False)
    email      = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30),nullable=False)
    last_name  = db.Column(db.String(30), nullable=False)




# class Feedback(db.Model):
#     __tablename__ = 'feedbacks'

