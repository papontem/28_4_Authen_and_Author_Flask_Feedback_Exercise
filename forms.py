from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length


class UserRegisterForm(FlaskForm):
    """form for when user first register"""
    username   = StringField("Username",   
                            validators=[
                                InputRequired(message="username cannot be blank"),
                                Length(max=20, message="Username cannot be over 20 chrs long")
                                ]
                            ) #20
    password   = PasswordField("Password", 
                            validators=[InputRequired(message="password cannot be blank")])
    
    email      = StringField("Email",       
                            validators=[
                                InputRequired(message="email cannot be blank"),
                                Email(message="Not a Valid Email"),
                                Length(max=50, message="Username cannot be over 50 chrs long")
                                ]
                            ) #50                    
    first_name = StringField("First Name", 
                            validators=[InputRequired(message="first name cannot be blank"),
                                Length(max=30, message="first name cannot be over 30 chrs long")
                                ]
                            )# 30
    last_name  = StringField("Last Name",  
                            validators=[InputRequired(message="last name cannot be blank"),
                                Length(max=30, message="last name cannot be over 30 chrs long")
                                ]
                            )# 30
class UserLoginForm(FlaskForm):
    """form for when user logs in"""

    username   = StringField("Username",   
                            validators=[
                                InputRequired(message="username cannot be blank"),
                                Length(max=20, message="Username cannot be over 20 chrs long")
                                ]
                            ) #20
    
    password   = PasswordField("Password", 
                            validators=[InputRequired(message="password cannot be blank")])

class FeedbackForm(FlaskForm):
    text = TextAreaField("Feedback Text",
                       validators=[InputRequired(message="Feedback cannot be blank")])
