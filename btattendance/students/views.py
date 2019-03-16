import os
from PIL import Image
from flask import (Blueprint, redirect, render_template,
                   url_for, flash, request)
from flask_login import login_user, current_user, login_required, logout_user
from btattendance.students.forms import (RegistrationForm, LoginForm,
                                         UpdateAccountForm, RequestResetForm,
                                         ResetPasswordForm)
from btattendance.models import Student, Department, DeptCode
from btattendance import db, mail
from secrets import token_hex
from flask_mail import Message
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


# here's some caching issue if image is saved with the same file name as
# previous the new image is not loaded from server as if it's still loading
# from cache so here i am using deleting the old file concept
def save_picture(form_image):
    old_file = current_user.profile_img
    random_name = token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    pic_name = random_name + f_ext    # gererating new random name

    dir_path = os.path.join(students.root_path, '../static/profile_students')
    pic_path = os.path.join(dir_path, pic_name)
    # deleting the old file
    if old_file != 'default.jpg':
        os.remove(os.path.join(dir_path, old_file))
    # save new file
    output_size = (125, 125)
    img = Image.open(form_image)
    img.thumbnail(output_size)
    img.save(pic_path)

    return pic_name


@students.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    image_file = url_for(
        'static', filename='profile_students/' + current_user.profile_img)
    if form.validate_on_submit():
        if form.picture.data:
            image_file = save_picture(form.picture.data)
            current_user.profile_img = image_file
        current_user.name = form.name.data
        current_user.bd_addr = form.bd_addr.data
        db.session.commit()
        flash('Account successfully updated', 'success')
        return redirect(url_for('students.account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.bd_addr.data = current_user.bd_addr

    return render_template('accountStu.html', form=form, image_file=image_file)


# Logout
@students.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('You are now logged out', category='info')

    return redirect(url_for('index'))


def send_reset_mail(student):
    token = student.get_reset_token()
    msg = Message(subject='Password Reset Request!',
                  sender='noreply@btattendance.com',
                  recipients=[student.email],
                  body=f'''To reset your password, visit the following link:
{url_for('students.reset_password', token=token, _external=True)}

If you didn't make this request then simply ignore this email and changes will be made!
''')
    mail.send(msg)


@students.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('students.dashboard'))
    form = RequestResetForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        send_reset_mail(student)
        flash('An email has been sent with the instructions to reset your password!', 'warning')
        return redirect(url_for('students.login'))

    return render_template('reset_request.html', title='Reset Password',
                           form=form)


@students.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('students.dashboard'))
    student = Student.verify_reset_token(token)
    if student is None:
        flash('The token is invalid or expired!', 'warning')
        return redirect(url_for('students.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        student.password_hash = student.generate_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset successfully! Please Login")
        return redirect(url_for('students.login'))

    return render_template('reset_password.html', title='Reset Password',
                           form=form)
