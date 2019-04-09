from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (BooleanField, PasswordField, SelectField, StringField,
                     SubmitField, ValidationError)
from wtforms.validators import DataRequired, Email, EqualTo, Length

from btattendance.models import DeptCode, Teacher


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


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        Email(),
        DataRequired()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# Update form when data is different from current user data
class UpdateAccountForm(FlaskForm):
    name = StringField('Name', validators=[
        Length(min=2, max=50),
        DataRequired()
    ])
    picture = FileField('Upload Profile Picture', validators=[
                        FileAllowed(['jpg', 'png', 'gif'])])
    submit = SubmitField('Update')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[
        Email(),
        DataRequired()
    ])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        if Teacher.query.filter_by(email=email.data).first() is None:
            raise ValidationError("This e-mail is not registered with us!")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=4, max=50)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords did not match!')
    ])
    submit = SubmitField('Reset Password')
