from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, Email


# Student Register Form Class
class Registration(FlaskForm):
    name = StringField('Name', validators=[Length(min=1, max=50), 
                                           DataRequired()])
    rollno = StringField('Rollno', validators=[Length(min=1, max=3),
                                               DataRequired()])
    email = StringField('Email', validators=[Email(), DataRequired()])
    macad = StringField('Macad', validators=[Length(max=17), DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')
