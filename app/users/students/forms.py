from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (BooleanField, PasswordField, SelectField, StringField,
                     SubmitField, ValidationError)
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

from app.models import Student, User
from app.utils import get_dept_name_value


# Student Register Form Class
class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[
        Length(min=2, max=50),
        DataRequired()
    ])
    rollno = StringField('Roll No.', validators=[
        Length(min=7, max=7),
        DataRequired(),
        Regexp('^[0-9]{3}[A-Z]{2}[0-9]{2}$', message="Roll No. format: '408CO15'")])  # noqa
    email = StringField('Email', validators=[
        Email(),
        DataRequired()
    ])
    bd_addr = StringField('Bluetooth Address', validators=[
        Length(min=17, max=17),
        DataRequired(),
        Regexp('^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$', message="Enter valid BD_ADDR [00:00:00:00:00:00]")  # noqa
    ])
    department = SelectField('Department', choices=get_dept_name_value())
    semester = SelectField('Semester', choices=[
                           (str(i), i) for i in range(1, 9)])
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
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("This e-mail is already registered with us!")

    def validate_rollno(self, rollno):
        if Student.query.filter_by(rollno=rollno.data).first():
            raise ValidationError(
                "Student with this rollno is already registered with us!")

    def validate_bd_addr(self, bd_addr):
        if Student.query.filter_by(bd_addr=bd_addr.data).first():
            raise ValidationError(
                "Bluetooth Address already registered with us!")


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
    bd_addr = StringField('Bluetooth Address', validators=[
        Length(min=17, max=17),
        DataRequired(),
        Regexp('^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$', message="Enter valid BD_ADDR [00:00:00:00:00:00]")  # noqa
    ])
    picture = FileField('Upload Profile Picture', validators=[
                        FileAllowed(['jpg', 'png', 'gif'])])
    submit = SubmitField('Update')

    def validate_bd_addr(self, bd_addr):
        if current_user.bd_addr != bd_addr.data:
            if Student.query.filter_by(bd_addr=bd_addr.data).first():
                raise ValidationError(
                    "Bluetooth Address already registered with us!")


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[
        Email(),
        DataRequired()
    ])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        if Student.query.filter_by(email=email.data).first() is None:
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
