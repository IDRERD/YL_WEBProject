from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    name = StringField("Product name", validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])
    count = IntegerField("Products count", validators=[DataRequired()], default=1)
    tags = SelectMultipleField("Tags", validators=[DataRequired()], choices=[("Flag1", "Flag1"), ("Flag2", "Flag2"), ("Flag3", "Flag3")])
    submit = SubmitField("Confirm")