import os
from secrets import token_hex

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from PIL import Image

from app import db
from app.models import Department, Student, Subject, Teacher, Attendance
from app.users.teachers.forms import (RegistrationForm, TakeAttendanceForm,
                                      UpdateAccountForm)
from utils import discover_bd

teachers = Blueprint('teachers', __name__)


# Register Teacher
@teachers.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        dept = Department.query.filter_by(
            dept_code=form.department.data).first()
        teacher = Teacher(name=form.name.data, email=form.email.data,
                          password=form.password.data, department=dept)
        db.session.add(teacher)
        db.session.commit()
        flash('Account created successfully! Please Log In.', 'success')
        return redirect(url_for('users.login'))
    return render_template('registerPro.html', form=form, title='Register')


# Check Attendance
@teachers.route('/check_attendance', methods=['GET', 'POST'])
@login_required
def check_attendance():
    if current_user.type != "teachers":
        return redirect(url_for('users.dashboard'))

    subjects = Subject.query.with_entities(Subject.subject_code).filter_by(teacher_id=current_user.id)   # noqa
    form = TakeAttendanceForm()
    form.subject.choices = [(s.subject_code, s.subject_code) for s in subjects]     # noqa

    if form.validate_on_submit():
        subject = Subject.query.filter_by(subject_code=form.subject.data).first()
        semester = subject.semester
        dept = subject.department_id
        students = Student.query.filter_by(semester=semester,
                                           department_id=dept)
        devices = discover_bd()
        for student in students:
            status = False
            if student.bd_addr in devices:
                status = True
            a = Attendance(status=status, semester=semester,
                           student_id=student.id, subject_id=subject.id)
            db.session.add(a)
            db.session.commit()
        return render_template('scan_prog.html', check=False, form=form)
    return render_template('scan_prog.html', check=True, form=form)


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
    user_type = current_user.type
    if user_type != "teachers":
        return redirect(url_for(f'{user_type}.account'))
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
