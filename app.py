from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import UserRegisterForm, UserLoginForm
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


##PART 3: MAKE ROUTES 
##GET /
@app.route('/')
def home_page():
    """ Get app homepage """

    return redirect("/register")

## GET AND POST /register
## GET /register
@app.route('/register', methods=["GET"])
def show_register_form():
    """
    Show a form that when submitted will register/create a user. 
    This form should accept a username, password, email, first_name, and last_name.
    Make sure you are using WTForms and that your password input hides the characters that the user is typing!
    """
    form = UserRegisterForm()
    return render_template("register.html", form=form)


## POST /register
@app.route('/register', methods=["POST"])
def register_form_submit():
    """
    Process the registration form by adding a new user. Then redirect to /secret
    """
    form = UserRegisterForm()

    if form.validate_on_submit():
        # gather the user data from the form
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        # create user instance
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        try:
            # attempt to add user to the database
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken. Please pick another')
            return render_template('register.html', form=form)

        # user added put username in session to keep them logged in.
        session['user_username'] = new_user.username
        flash('Welcome! Successfully Created Your Account!', "success")

        return redirect('/secret')
    else:
        # handle form validation errors
        flash("Invalid input data. Please check your form.", "warning")

    return render_template("register.html", form=form)



## GET AND POST /login
# GET /login 
@app.route("/login")
def show_login_form():
    """
    Show a form that when submitted will login a user.
    This form should accept a username and a password.
    
    Make sure you are using WTForms and that your password input hides the characters that the user is typing!
    """
    form = UserLoginForm()
    return render_template("login.html", form=form)


# POST /login
@app.route("/login", methods=["POST"])
def login_form_submit():
    """
        handle login form submission.
        Process the login form, ensuring the user is authenticated and going to /secret if so.
    """

    form = UserLoginForm()

    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, password)

        if user:
            # keep logged in
            session["user_username"] = user.username 
            return redirect("/secret")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)

# Part 4
## GET /secret
@app.route("/secret")
def secret():
    """
        Hidden page for logged-in users only.
        Dont let everyone go to /secret
    """

    if "user_username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

        # alternatively, can return HTTP Unauthorized status:
        #
        # from werkzeug.exceptions import Unauthorized
        # raise Unauthorized()

    else:
        return render_template("secret.html")


# Part 5: Log out users
# Make routes for the following:
##GET /logout
@app.route("/logout")
def logout():
    """
        Clear any information from the session and redirect to /
    """
    session.pop("user_username")
    flash("Goodbye!", "success")
    return redirect("/")

