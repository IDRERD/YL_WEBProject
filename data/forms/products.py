from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    name = StringField("Product name", validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])
    count = IntegerField("Quantity", validators=[DataRequired()], default=1)
    submit = SubmitField("Confirm")