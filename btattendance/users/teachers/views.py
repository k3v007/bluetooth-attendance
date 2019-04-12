import os
from secrets import token_hex

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message
from PIL import Image

from btattendance import db, mail
from btattendance.models import Department, DeptCode, Teacher
from btattendance.users.teachers.forms import (RegistrationForm,
                                               UpdateAccountForm)

teachers = Blueprint('teachers', __name__)


# Register Teacher
@teachers.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('teachers.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        dept = Department.query.filter_by(
            dept_code=DeptCode[form.department.data]).first()
        teacher = Teacher(name=form.name.data, email=form.email.data,
                          password=form.password.data, department=dept)
        db.session.add(teacher)
        db.session.commit()
        flash('Account created successfully! Please Log In.', 'success')
        return redirect(url_for('teachers.login'))
    return render_template('registerPro.html', form=form, title='Register')


# Teacher dashboard
@teachers.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboardPro.html')


# # Check Attendance
# @teachers.route('/check_attendance')
# @is_logged_in
# def check_attendance():
#     sub = session['subject']  
#     # DB task
#     # result = cur.execute("SELECT bd_addr FROM students")
#     result = []
#     cur = []
#     bd_addrs = cur.fetchall()

#     print(bd_addrs)
#     if result > 0:
#         print("Hello1")
#         # bluescan.delay(bd_addrs, sub)
#         return render_template('scan_prog.html')
#     else:
#         msg = 'No Records Found'
#         return render_template('dashboardPro.html', msg=msg)


# # Delete Attendance
# @teachers.route('/delete_attendance/<string:id>', methods=['POST'])
# @is_logged_in
# def delete_attendance(id):
#     # DB task
#     flash('Attendance Deleted', 'success')

#     return redirect(url_for('teachers.dashboard'))


# here's some caching issue if image is saved with the same file name as
# previous the new image is not loaded from server as if it's still loading
# from cache so here i am using deleting the old file concept
def save_picture(form_image):
    old_file = current_user.profile_img
    random_name = token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    pic_name = random_name + f_ext    # gererating new random name

    dir_path = os.path.join(teachers.root_path, '../static/profile_teachers')
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


@teachers.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    image_file = url_for(
        'static', filename='profile_teachers/' + current_user.profile_img)
    if form.validate_on_submit():
        if form.picture.data:
            image_file = save_picture(form.picture.data)
            current_user.profile_img = image_file
        current_user.name = form.name.data
        db.session.commit()
        flash('Account successfully updated', 'success')
        return redirect(url_for('teachers.account'))
    elif request.method == 'GET':
        form.name.data = current_user.name

    return render_template('accountPro.html', form=form, image_file=image_file)
