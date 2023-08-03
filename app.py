from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import UserRegisterForm, UserLoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError
import traceback
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

# APP SQLAlchemy INIT
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
    Process the registration form by adding a new user. Then redirect to /users/<username>
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
        # take user to their new profile page
        return redirect(f"/users/{new_user.username}")
    else:
        # handle form validation errors
        flash("Invalid input data. Please check your form.", "warning")

    return render_template("register.html", form=form)



## GET AND POST /login
## GET /login 
@app.route("/login", methods=["GET"])
def show_login_form():
    """
    Show a form that when submitted will login a user.
    This form should accept a username and a password.
    
    Make sure you are using WTForms and that your password input hides the characters that the user is typing!
    """
    form = UserLoginForm()
    return render_template("login.html", form=form)


## POST /login
@app.route("/login", methods=["POST"])
def login_form_submit():
    """
        handle login form submission.
        Process the login form, ensuring the user is authenticated and going to /users/<username> if so.
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
            # take user to their profile page
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)

## Part 4: /secret
## Part 6: changed /secret to /users/<username>
## Part 8: Make/Modify Routes For Users and Feedback
## GET /users/<username>
@app.route("/users/<username>")
def show_user_profile(username):
    """
        Hidden page for logged-in users only.
        Dont let everyone go to /users/<username>

        Display a template the shows information about that user (everything except for their password)
        You should ensure that only logged in users can access this page.
    
        Show all of the feedback that the user has given.
        For each piece of feedback, display with a link to a form to edit the feedback and a button to delete the feedback.
        Have a link that sends you to a form to add more feedback and a button to delete the user.
    """
    
    if "user_username" not in session:

        flash("You must be logged in to view!", "danger")
        return redirect("/")

        # alternatively, can return HTTP Unauthorized status:
        # from werkzeug.exceptions import Unauthorized; raise Unauthorized()

    else:

        user = User.query.get_or_404(username)
        
        return render_template("user_profile.html", user=user)


## Part 5: Log out users
##GET /logout
@app.route("/logout")
def logout():
    """
        Clear any information from the session and redirect to /
    """
    session.pop("user_username")
    flash("Goodbye!", "success")
    return redirect("/")


## Part 8: Make/Modify Routes For Users and Feedback
## GET /users/<username>/feedback/add
@app.route("/users/<username>/feedback/add", methods=["GET"])
def show_add_feedback_form(username):
    """
        Display a form to add feedback
        Make sure that only the user who is logged in can see this form.
    """
    if "user_username" not in session:

        flash("You must be logged in to add feedback!", "danger")
        return redirect("/")

        # alternatively, can return HTTP Unauthorized status:
        # from werkzeug.exceptions import Unauthorized; raise Unauthorized()

    # MAKING SURE RIGHT USER IS IN THE RIGHT FORM
    user = User.query.get_or_404(username)

    if user.username != session["user_username"]:
        flash("You are not allowed there! Acces Denied!", "danger")
        return redirect("/")

        # alternatively, can return HTTP Unauthorized status:
        # from werkzeug.exceptions import Unauthorized; raise Unauthorized()
    else:
        form = FeedbackForm()
        return render_template("add_feedback.html", form=form, user=user)
    

## POST /users/<username>/feedback/add
@app.route("/users/<username>/feedback/add", methods=["POST"])
def feedback_form_submit(username):
    """
        Process the add feedback form by adding a new feedback record. 
        Add a new piece of feedback and redirect to /users/<username>
        Make sure that only the user who is logged in can successfully add feedback
    """
    if "user_username" not in session:

        flash("You must be logged in to add feedback!", "danger")
        return redirect("/")

        # alternatively, can return HTTP Unauthorized status:
        # from werkzeug.exceptions import Unauthorized; raise Unauthorized()

    user = User.query.get_or_404(session["user_username"])
    form = FeedbackForm()

    if form.validate_on_submit():
        # gather the feedback data from the form
        title = form.title.data
        content = form.content.data

        # create feedback instance
        new_feedback = Feedback(title=title,content=content,username=user.username)
        db.session.add(new_feedback)
        try:
            # attempt to add feedback to the database
            db.session.commit()
        except Exception as e:

            print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            print("Exception Error in attempt to add feedback ")
            print("An exception occurred:")
            print("Type:", type(e).__name__)
            print("Value:", str(e))
            print("Traceback:", traceback.format_exc())
            print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")

            return render_template("add_feedback.html", form=form, user=user)

        flash('Successfully Added Feedback!', "success")
        # take user to their profile page to see feedback list
        return redirect(f"/users/{user.username}")
    else:
        # handle form validation errors
        flash("Invalid input data. Please check your form.", "warning")
        return render_template("add_feedback.html", form=form, user=user)
        
        

    

# POST /users/<username>/delete
    # Remove the user from the database and make sure to also delete all of their feedback. 
    # Clear any user information in the session and redirect to /.
    # Make sure that only the user who is logged in can successfully delete their account.

# GET /feedback/<feedback-id>/update
    # Display a form to edit feedback — **Make sure that only the user who has written that feedback can see this form **

# POST /feedback/<feedback-id>/update
    # Update a specific piece of feedback and redirect to /users/<username> — Make sure that only the user who has written that feedback can update it

# POST /feedback/<feedback-id>/delete
    # Delete a specific piece of feedback and redirect to /users/<username> — Make sure that only the user who has written that feedback can delete it 