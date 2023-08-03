"""Models for authen. author. app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

## Part 1: Create User Model
class User(db.Model):
    """
       Model for Users who register and login to app
       - username   - a unique primary key that is no longer than 20 characters.
       - password   - a not-nullable column that is text
       - email      - a not-nullable column that is unique and no longer than 50 characters.
       - first_name - a not-nullable column that is no longer than 30 characters.
       - last_name  - a not-nullable column that is no longer than 30 characters
    """
    __tablename__ = 'users'

    username   = db.Column(db.String(20), primary_key=True) 
    password   = db.Column(db.String,     nullable=False)
    email      = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name  = db.Column(db.String(30), nullable=False)


    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)

        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed password
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False

## Part 7: Create a Feedback model 
class Feedback(db.Model):
    """ 
        Model for Feedbacks given by users
        - id       - a unique primary key that is an auto incrementing integer
        - title    - a not-nullable column that is at most 100 characters
        - content  - a not-nullable column that is text
        - username - a foreign key that references the username column in the users table
    """
    __tablename__ = 'feedbacks'

    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title    = db.Column(db.String(100), nullable=False)
    content  = db.Column(db.Text, nullable=False)
    username = db.Column(db.String, db.ForeignKey('users.username'))
    
    # Relations: when user is deleted, delete all of their feedbacks aswell
    user = db.relationship('User', backref=db.backref("feedbacks", cascade="all, delete-orphan"))



    


