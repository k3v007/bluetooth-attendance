from flask import (Blueprint, redirect, render_template, request,
                   url_for, flash, session)
from btattendance.utils import is_logged_in
from btattendance.teachers.forms import Registration

teachers = Blueprint('teachers', __name__)


# Professor Register
@teachers.route('/register', methods=['GET', 'POST'])
def register():
    form = Registration(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        password = form.password.data

        # DB task
        # cur.execute("INSERT INTO professors(name, email, subject, password)
        # VALUES(%s, %s, %s, %s)", (name, email, subject, password))
        flash('You are now registered and can log in', 'success')

        return redirect(url_for('teachers.login'))
    return render_template('registerPro.html', form=form)


# Professor login
@teachers.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']

        # DB task
        # result = cur.execute("SELECT * FROM professors WHERE 
        # email = %s", [email])
        result = []
        cur = []

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']
            username = data['name']
            sub = data['subject']
            # Compare Passwords
            if result.check_password(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                session['student'] = False
                session['subject'] = sub

                flash('You are now logged in', 'success')
                return redirect(url_for('teachers.dashboard'))
            else:
                error = 'Invalid login'
                return render_template('loginPro.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('loginPro.html', error=error)

    return render_template('loginPro.html')


# Dashboard Professors
@teachers.route('/dashboard')
@is_logged_in
def dashboard():
    subject = session['subject']
    # DB task
    result = []
    cur = []
    # result = cur.execute("SELECT name, attendance.id, subject, presabs,
    # class_date FROM students, attendance WHERE attendance.macad =
    # students.macad and subject = %s", [subject])

    if result > 0:
        return render_template('dashboardPro.html', attends=attends)
    else:
        msg = 'No Attendance Found'
        return render_template('dashboardPro.html', msg=msg)
    # Close connection
    cur.close()


# Check Attendance
@teachers.route('/check_attendance')
@is_logged_in
def check_attendance():
    sub = session['subject']  
    # DB task
    # result = cur.execute("SELECT macad FROM students")
    result = []
    cur = []
    macads = cur.fetchall()

    print(macads)
    if result > 0:
        print("Hello1")
        # bluescan.delay(macads, sub)
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