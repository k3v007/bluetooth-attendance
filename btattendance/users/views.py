from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, logout_user
from flask_mail import Message

from btattendance import admin, db, mail
from btattendance.models import (Attendance, Course, Department, Section,
                                 Student, Teacher)
from btattendance.users.forms import (LoginForm, RequestResetForm,
                                      ResetPasswordForm)

users = Blueprint("users", __name__)


# Student login
@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.type == "student":
            return redirect(url_for('students.dashboard'))
        else:
            return redirect(url_for('teachers.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Student.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome {user.name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('students.dashboard'))
        else:
            flash(f'Invalid username or password!', category='danger')
    return render_template('login.html', form=form, title='Login')


# Logout
@users.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('You are now logged out', category='info')

    return redirect(url_for('index'))


def send_reset_mail(teacher):
    token = teacher.get_reset_token()
    msg = Message(subject='Password Reset Request!',
                  sender='noreply@btattendance.com',
                  recipients=[teacher.email],
                  body=f'''To reset your password, visit the following link:
{url_for('teachers.reset_password', token=token, _external=True)}

If you didn't make this request then simply ignore this email and changes will be made!
''')
    mail.send(msg)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('students.dashboard'))
    form = RequestResetForm()
    if form.validate_on_submit():
        teacher = Teacher.query.filter_by(email=form.email.data).first()
        send_reset_mail(teacher)
        flash('An email has been sent with the instructions to reset your password!', 'warning')
        return redirect(url_for('teachers.login'))

    return render_template('reset_request.html', title='Reset Password',
                           form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('teachers.dashboard'))
    teacher = Teacher.verify_reset_token(token)
    if teacher is None:
        flash('The token is invalid or expired!', 'warning')
        return redirect(url_for('teachers.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        teacher.password_hash = teacher.generate_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset successfully! Please Login")
        return redirect(url_for('teachers.login'))

    return render_template('reset_password.html', title='Reset Password',
                           form=form)


# add view for admin
admin.add_views(
    ModelView(Department, db.session),
    ModelView(Student, db.session),
    ModelView(Teacher, db.session),
    ModelView(Course, db.session),
    ModelView(Section, db.session),
    ModelView(Attendance, db.session),
)
