from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class BuyForm(FlaskForm):
    buy = SubmitField("Buy")