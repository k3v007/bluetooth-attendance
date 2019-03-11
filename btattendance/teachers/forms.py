from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


# Professor Register Form Class
class Registration(FlaskForm):
    name = StringField('Name', [Length(min=1, max=50), DataRequired()])
    email = StringField('Email', [Email(), DataRequired()])
    subject = StringField('Subject', [Length(min=1, max=17), DataRequired()]) # noqa
    password = PasswordField('Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
