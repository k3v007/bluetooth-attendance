from flask import Blueprint
from flask_admin.contrib.sqla import ModelView

from app import admin, db
from app.models import Attendance, Department, Student, Subject, Teacher

administrator = Blueprint(__name__, "administrator")


class DepartmentModelView(ModelView):
    can_export = True
    column_list = ('dept_name', 'dept_code', 'hod', 'hod_email')
    column_labels = dict(dept_name='Department',
                         dept_code='Code',
                         hod='Head of Department',
                         hod_email='HOD Email')
    column_default_sort = 'dept_code'
    column_sortable_list = ('dept_name', 'dept_code', 'hod')
    column_filters = ('dept_name', 'hod', 'hod_email')
    form_columns = ('dept_name', 'dept_code', 'hod', 'hod_email')


class StudentModelView(ModelView):
    column_list = ('rollno', 'name', 'email', 'active', 'semester', 'bd_addr',
                   'profile_img', 'department')
    column_exclude_list = ('password', 'type')
    column_filters = ('name', 'email', 'active')
    column_labels = dict(rollno='Roll No.',
                         profile_img='Profile Image',
                         bd_addr='Bluetooth Address')
    column_sortable_list = ('rollno', 'name', 'semester', 'active')
    column_default_sort = 'rollno'
    can_create = False
    form_excluded_columns = ('type',)
    form_widget_args = {
        'password': {
            'readonly': True
        },
    }


class TeacherModelView(ModelView):
    column_list = ('name', 'email', 'active', 'profile_img', 'department',
                   'subjects')
    column_exclude_list = ('password', 'type')
    column_filters = ('name', 'email', 'active')
    column_labels = dict(profile_img='Profile Image')
    column_sortable_list = ('name', 'active')
    column_default_sort = 'name'
    can_create = False
    form_excluded_columns = ('type',)
    form_widget_args = {
        'password': {
            'readonly': True
        },
    }


class SubjectModelView(ModelView):
    column_list = ('subject_code', 'name', 'semester', 'teacher', 'department')
    form_columns = ('subject_code', 'name', 'semester', 'teacher',
                    'department')
    column_filters = ('name', 'subject_code', 'semester')
    column_labels = dict(subject_code='Code',)
    column_default_sort = 'semester'
    column_sortable_list = ('name', 'subject_code', 'semester')


class AttendanceModelView(ModelView):
    can_export = True
    column_list = ('date', 'status', 'semester', 'student', 'subject')
    column_filters = ('date', 'status', 'semester')
    column_default_sort = 'date'
    column_sortable_list = ('date', 'status', 'semester')
    form_columns = ('date', 'status', 'semester', 'student', 'subject')


# add view for admin
admin.add_views(
    DepartmentModelView(Department, db.session),
    StudentModelView(Student, db.session),
    TeacherModelView(Teacher, db.session),
    SubjectModelView(Subject, db.session),
    AttendanceModelView(Attendance, db.session),
)
