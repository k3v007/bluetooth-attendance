from flask import (Blueprint, redirect, render_template, request,
                   url_for, flash, session)
from btattendance.utils import is_logged_in
from btattendance.students.forms import Registration


students = Blueprint('students', __name__)

# Student Register
@students.route('/register', methods=['GET', 'POST'])
def register():
    form = Registration(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        rollno = form.rollno.data
        macad = form.macad.data
        password = form.password.data

        # DB task

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('students.login'))
    return render_template('registerStu.html', form=form)


# Student login
@students.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']

        # DB TASK
        cur = []
        result = []

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']
            username = data['name']
            macadd = data['macad']

            # Compare Passwords
            # check_password is a function in model
            if result.check_password(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                session['student'] = True
                session['macaddress'] = macadd
                
                flash('You are now logged in', 'success')
                return redirect(url_for('students.dashboard'))
            else:
                error = 'Invalid login'
                return render_template('loginStu.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('loginStu.html', error=error)

    return render_template('loginStu.html')


@students.route('/dashboard')
@is_logged_in
def dashboard():  
    macadress = session['macaddress']
    # DB task
    # result = cur.execute("SELECT * FROM attendance WHERE macad = %s", [macadress])
    result = []
    cur = []

    attends = cur.fetchall()

    print(attends)

    if result > 0:
        return render_template('dashboardStu.html', attends=attends)
    else:
        msg = 'No Attendance Found'
        return render_template('dashboardStu.html', msg=msg)


# Logout
@students.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))