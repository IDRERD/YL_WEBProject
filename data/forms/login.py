from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Sing in")