from flask_wtf import FlaskForm
from wtforms import (BooleanField, PasswordField, StringField, SubmitField,
                     ValidationError)
from wtforms.validators import DataRequired, Email, EqualTo, Length

from btattendance.models import User


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


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[
        Email(),
        DataRequired()
    ])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first() is None:
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
