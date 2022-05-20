from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired


class StudentForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    interests = SelectMultipleField(
        'interests', validators=[DataRequired()],
        choices=[]
    )


class InterestForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
