from flask import (Blueprint, redirect, render_template,
                   url_for, flash, session)
from btattendance.utils import is_logged_in
from btattendance.teachers.forms import RegistrationForm, LoginForm

teachers = Blueprint('teachers', __name__)


# Professor Register
@teachers.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        password = form.password.data

        # DB task
        # cur.execute("INSERT INTO professors(name, email, subject, password)
        # VALUES(%s, %s, %s, %s)", (name, email, subject, password))
        flash('You are now registered and can log in', 'success')

        return redirect(url_for('teachers.login'))
    return render_template('registerPro.html', form=form, title='Register')


# Professor login
@teachers.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('teachers.dashboard'))

    return render_template('loginPro.html', form=form, title='Log In')


# Dashboard Professors
@teachers.route('/dashboard')
@is_logged_in
def dashboard():
    # DB task
    
    # result = cur.execute("SELECT name, attendance.id, subject, presabs,
    # class_date FROM students, attendance WHERE attendance.bd_addr =
    # students.bd_addr and subject = %s", [subject])

    return render_template('dashboardPro.html')
    # Close connection


# Check Attendance
@teachers.route('/check_attendance')
@is_logged_in
def check_attendance():
    sub = session['subject']  
    # DB task
    # result = cur.execute("SELECT bd_addr FROM students")
    result = []
    cur = []
    bd_addrs = cur.fetchall()

    print(bd_addrs)
    if result > 0:
        print("Hello1")
        # bluescan.delay(bd_addrs, sub)
        return render_template('scan_prog.html')
    else:
        msg = 'No Records Found'
        return render_template('dashboardPro.html', msg=msg)


# Delete Attendance
@teachers.route('/delete_attendance/<string:id>', methods=['POST'])
@is_logged_in
def delete_attendance(id):
    # DB task
    flash('Attendance Deleted', 'success')

    return redirect(url_for('teachers.dashboard'))


# Logout
@teachers.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))