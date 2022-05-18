from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, IntegerField
from wtforms.validators import DataRequired

class StudentForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    interests = FieldList(IntegerField('Interest'), min_entries=1, max_entries=5)

class InterestForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])