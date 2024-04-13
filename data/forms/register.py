from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_again = PasswordField("Repeat the password", validators=[DataRequired()])
    name = StringField("User name", validators=[DataRequired()])
    submit = SubmitField("Sing up")