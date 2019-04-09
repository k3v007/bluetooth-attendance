from flask import Blueprint
from flask_admin.contrib.sqla import ModelView

from btattendance import admin, db
from btattendance.models import (Attendance, Course, Department, Section,
                                 Student, Teacher)

users = Blueprint("users", __name__)

# add view for admin
admin.add_views(
    ModelView(Department, db.session),
    ModelView(Student, db.session),
    ModelView(Teacher, db.session),
    ModelView(Course, db.session),
    ModelView(Section, db.session),
    ModelView(Attendance, db.session),
)
