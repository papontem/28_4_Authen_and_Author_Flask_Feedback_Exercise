from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import UserForm
from sqlalchemy.exc import IntegrityError
from secrets import app_secret_key

app = Flask(__name__)

# Flask-SQLALchemy settings
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

# Flask-DTB settings
app.config["SECRET_KEY"] = app_secret_key
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

#APP sqlAlchemy INIT
connect_db(app)
db.create_all()

#GET /
@app.route('/')
def home_page():
    """ Get app homepage """

    flash("HELOOOOO","danger")
    flash("HELOOOOO","success")
    return render_template('home.html')

