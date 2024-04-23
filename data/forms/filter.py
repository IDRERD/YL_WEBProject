from flask_wtf import *
from wtforms import *
from wtforms.validators import DataRequired


class FilterForm(FlaskForm):
    order = SelectField("Order by", choices=["Latest", "Biggest price", "Most in stock"])