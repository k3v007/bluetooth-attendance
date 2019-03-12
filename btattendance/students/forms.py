from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Email, Regexp


# Student Register Form Class
class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[
        Length(min=2, max=50),
        DataRequired()
    ])
    rollno = StringField('Roll No.', validators=[
        Length(min=7, max=7),
        DataRequired(),
        Regexp('^[0-9]{3}[A-Z]{2}[0-9]{2}$', message="Roll No. format: '408CO15'")]) # noqa
    email = StringField('Email', validators=[
        Email(),
        DataRequired()
    ])
    bd_addr = StringField('Bluetooth Address', validators=[
        Length(min=17, max=17),
        DataRequired(),
        Regexp('^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$', message="Enter valid BD_ADDR [00:00:00:00:00:00]")  # noqa
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=4, max=50)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords did not match!')
    ])
    submit = SubmitField('Sign Up')


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
