from flask import (Blueprint, redirect, render_template,
                   url_for, flash, session)
from btattendance.utils import is_logged_in
from btattendance.students.forms import RegistrationForm, LoginForm


students = Blueprint('students', __name__)

# Student Register
@students.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        rollno = form.rollno.data
        bd_addr = form.bd_addr.data
        password = form.password.data
        # DB task

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('students.login'))
    return render_template('registerStu.html', form=form, title='Register')


# Student login
@students.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('students.dashboard'))
    return render_template('loginStu.html', form=form, title='Login')


@students.route('/dashboard')
@is_logged_in
def dashboard():  
    return render_template('dashboardStu.html')


# Logout
@students.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))