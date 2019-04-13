import os
from secrets import token_hex

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from PIL import Image

from app import db
from app.models import Department, DeptCode, Student
from app.users.students.forms import RegistrationForm, UpdateAccountForm


students = Blueprint('students', __name__)


# Student Register
@students.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        dept = Department.query.filter_by(
            dept_code=DeptCode[form.department.data]).first()
        student = Student(name=form.name.data, rollno=form.rollno.data,
                          email=form.email.data, password=form.password.data,
                          bd_addr=form.bd_addr.data, department=dept,
                          semester=form.semester.data)
        db.session.add(student)
        db.session.commit()
        flash('Account created successfully! Please Log In.', 'success')
        return redirect(url_for('users.login'))
    return render_template('registerStu.html', form=form, title='Register')


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
    user_type = current_user.type
    if user_type != "students":
        return redirect(url_for(f'{user_type}.account'))
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
