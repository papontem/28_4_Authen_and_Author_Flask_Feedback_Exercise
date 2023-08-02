from flask import Flask, request, render_template, redirect, session, flash
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


# PART 3: MAKE ROUTES 

#GET /
@app.route('/')
def home_page():
    """ Get app homepage """

    return redirect("/register")

# GET AND POST /register
@app.route('/register', methods=["GET","POST"])
def register_form():
    """ 
        Get user register/signup form 
            Show a form that when submitted will register/create a user. 
            This form should accept a username, password, email, first_name, and last_name.
            Make sure you are using WTForms and that your password input hides the characters that the user is typing!

        Post register/signup form
            Process the registration form by adding a new user. Then redirect to /secret
    """
    form = UserForm()

    if request.method == 'GET':
        # Code to handle GET requests
        # flash("This is a GET request")

        return render_template("register.html", form=form)
    
    elif request.method == 'POST' and form.validate_on_submit():
        # Code to handle POST requests

        # gather the user data from from
        username   = form.username.data
        password   = form.password.data
        email      = form.email.data   
        first_name = form.first_name.data  
        last_name  = form.last_name.data 

        # create user instance
        new_user = User.register( username, password, email, first_name, last_name)
        db.session.add(new_user)
        try:
            # attempt to add user to database
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
        # user added put id in session to keep them logged in.
        session['user_username'] = new_user.username
        flash('Welcome! Successfully Created Your Account!', "success")
        # 
        return redirect('/secret')
    
    else:
        # Code to handle other request methods (if any)
        flash("Unsupported request method", "warning")
    
    return render_template("register.html")

@app.route("/secret")
def secret():
    """Example hidden page for logged-in users only."""

    if "user_username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

        # alternatively, can return HTTP Unauthorized status:
        #
        # from werkzeug.exceptions import Unauthorized
        # raise Unauthorized()

    else:
        return render_template("secret.html")


# GET /login

#     Show a form that when submitted will login a user. This form should accept a username and a password.

#     Make sure you are using WTForms and that your password input hides the characters that the user is typing!


# POST /login
#     Process the login form, ensuring the user is authenticated and going to /secret if so.
