from flask import (Blueprint, redirect, render_template,
                   url_for, flash, session, request)
from flask_login import login_user, current_user, login_required, logout_user
from btattendance.utils import is_logged_in
from btattendance.students.forms import RegistrationForm, LoginForm
from btattendance.models import Student, Department, DeptCode
from btattendance import db


students = Blueprint('students', __name__)

# Student Register
@students.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('students.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        dept = Department.query.filter_by(
            dept_code=DeptCode[form.department.data]).first()
        student = Student(name=form.name.data, rollno=form.rollno.data,
                          email=form.email.data, password=form.password.data,
                          bd_addr=form.bd_addr.data,
                          department=dept)
        db.session.add(student)
        db.session.commit()
        flash('Account created successfully! Please Log In.', 'success')
        return redirect(url_for('students.login'))
    return render_template('registerStu.html', form=form, title='Register')


# Student login
@students.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('students.dashboard'))
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
    return render_template('loginStu.html', form=form, title='Login')


# Student dashboard
@students.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboardStu.html')


# Logout
@students.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('You are now logged out', category='info')

    return redirect(url_for('index'))
