from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (PasswordField, SelectField, StringField, SubmitField,
                     ValidationError)
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.models import DeptCode, Teacher


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[
        Length(min=2, max=50),
        DataRequired()
    ])
    email = StringField('Email', validators=[
        Email(),
        DataRequired()
    ])
    department = SelectField('Department', choices=[
                             (d.name, d.value) for d in DeptCode])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=4, max=50)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords did not match!')
    ])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        if Teacher.query.filter_by(email=email.data).first():
            raise ValidationError("This e-mail is already registered with us!")


# Update form when data is different from current user data
class UpdateAccountForm(FlaskForm):
    name = StringField('Name', validators=[
        Length(min=2, max=50),
        DataRequired()
    ])
    picture = FileField('Upload Profile Picture', validators=[
                        FileAllowed(['jpg', 'png', 'gif'])])
    submit = SubmitField('Update')
