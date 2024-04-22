from flask_wtf import *
from wtforms import *
from wtforms.validators import DataRequired


class TagForm(FlaskForm):
    tag_name = StringField("Tag name", validators=[DataRequired()])
    submit = SubmitField("Add tag")