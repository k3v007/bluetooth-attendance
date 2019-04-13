import enum
import os
from datetime import datetime

from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class DeptCode(enum.Enum):
    bt = 'Bio-technology'
    coe = 'Computer Engineering'
    ece = 'Electronics and Communication Engineering'
    ice = 'Instrumentation and Control Engineering'
    it = 'Information Technology'
    me = 'Mechanical Engineering'


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    dept_code = db.Column(db.Enum(DeptCode), nullable=False)
    hod = db.Column(db.String(50), nullable=False, unique=True)
    hod_email = db.Column(db.String(80), nullable=False, unique=True)
    students = db.relationship('Student', backref='department', lazy=True)
    teachers = db.relationship('Teacher', backref='department', lazy=True)
    courses = db.relationship('Course', backref='department', lazy=True)

    def __init__(self, dept_code, hod, hod_email):
        self.dept_code = DeptCode[dept_code]
        self.hod = hod
        self.hod_email = hod_email

    def __repr__(self):
        return f"Department({self.dept_code}', '{self.hod}', '{self.hod_email}')"


registration = db.Table('registration_info',
                        db.Column('student_id', db.Integer, db.ForeignKey(
                            'students.id'), primary_key=True),
                        db.Column('section_id', db.Integer, db.ForeignKey(
                            'sections.id'), primary_key=True)
                        )


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    type = db.Column(db.String(20), default="user")
    __mapper_args__ = {
        'polymorphic_identity': 'users',
        'polymorphic_on': type
    }

    def generate_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(os.environ.get('SECRET_KEY'), expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @classmethod
    def verify_reset_token(cls, token):
        s = Serializer(os.environ.get('SECRET_KEY'))
        try:
            user_id = s.loads(token)['user_id']
        except:     # noqa
            return None
        return cls.query.get(user_id)


class Student(User):
    __tablename__ = 'students'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    rollno = db.Column(db.String(7), nullable=False, unique=True)
    profile_img = db.Column(db.String(50), nullable=False,
                            default='default.jpg')
    bd_addr = db.Column(db.String(90), nullable=False, unique=True)
    semester = db.Column(db.Integer, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey(
                             'departments.id'), nullable=False)
    attendance = db.relationship('Attendance', backref='student', lazy=True)
    registration_info = db.relationship('Section', secondary=registration,
                                        lazy='subquery',
                                        backref=db.backref(
                                            'department', lazy=True)
                                        )
    __mapper_args__ = {
        'polymorphic_identity': 'students',
    }

    def __init__(self, name, rollno, email, password, bd_addr, department,
                 semester):
        self.name = name
        self.rollno = rollno
        self.email = email
        self.password_hash = self.generate_password(password)
        self.bd_addr = bd_addr
        self.department_id = department.id
        self.semester = semester

    def __repr__(self):
        return f"Student('{self.name}', '{self.rollno}', '{self.email}', '{self.bd_addr}',\
                '{self.department_id}', '{self.semester}')"


class Teacher(User):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    profile_img = db.Column(db.String(50), nullable=False,
                            default='default.jpg')
    sections = db.relationship('Section', backref='teacher', lazy=True)
    department_id = db.Column(db.Integer, db.ForeignKey(
        'departments.id'), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'teachers',
    }

    def __init__(self, name, email, password, department):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.department_id = department.id

    def __repr__(self):
        return f"Teacher('{self.name}', '{self.email}', '{self.department_id}')"  # noqa


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(5), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    credit = db.Column(db.Integer, nullable=False)
    sections = db.relationship('Section', backref='course', lazy=True)
    department_id = db.Column(db.Integer, db.ForeignKey(
        'departments.id'), nullable=False)

    def __init__(self, course_code, name, credit, department):
        self.course_code = course_code
        self.name = name
        self.credit = credit
        self.department_id = department.id

    def __repr__(self):
        return f"Course('{self.course_code}', '{self.name}', '{self.credit}', '{self.department_id}')"  # noqa


class Section(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key=True)
    semester = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey(
        'courses.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey(
        'teachers.id'), nullable=False)
    attendance = db.relationship('Attendance', backref='section', lazy=True)

    def __init__(self, semester, course, teacher):
        self.semester = semester
        self.course_id = course.id
        self.teacher_id = teacher.id

    def __repr__(self):
        return f"Subject({self.semester}, {self.course_id}, {self.teacher_id})"


class Status(enum.Enum):
    abs = 'absent'
    pres = 'present'


class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Enum(Status), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey(
        'students.id'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey(
        'sections.id'), nullable=False)

    def __init__(self, date, status, student, section):
        self.date = date
        self.status = status
        self.student_id = student.id
        self.section_id = section.id

    def __repr__(self):
        return f"Subject({self.date}, {self.status}, {self.student_id}, {self.section_id})"
