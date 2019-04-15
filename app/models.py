import os
from datetime import datetime

from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    dept_code = db.Column(db.String(5), nullable=False)
    dept_name = db.Column(db.String(100), nullable=False)
    hod = db.Column(db.String(50), nullable=False, unique=True)
    hod_email = db.Column(db.String(80), nullable=False, unique=True)
    students = db.relationship('Student', backref='department', lazy=True)
    teachers = db.relationship('Teacher', backref='department', lazy=True)
    subjects = db.relationship('Subject', backref='department', lazy=True)

    def __repr__(self):
        return f"{self.dept_name} ({self.dept_code})"


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    type = db.Column(db.String(20), default="user")
    __mapper_args__ = {
        'polymorphic_identity': 'users',
        'polymorphic_on': type
    }

    def generate_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

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
    __mapper_args__ = {
        'polymorphic_identity': 'students',
    }

    def __init__(self, name, rollno, email, password, bd_addr, department,
                 semester):
        self.name = name
        self.rollno = rollno
        self.email = email
        self.password = self.generate_password(password)
        self.bd_addr = bd_addr
        self.department_id = department.id
        self.semester = semester

    def __repr__(self):
        return f"{self.name} ({self.rollno})"


class Teacher(User):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    profile_img = db.Column(db.String(50), nullable=False,
                            default='default.jpg')
    subjects = db.relationship('Subject', backref='teacher', lazy=True)
    department_id = db.Column(db.Integer, db.ForeignKey(
        'departments.id'), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'teachers',
    }

    def __init__(self, name, email, password, department):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.department_id = department.id

    def __repr__(self):
        return f"{self.name} ({self.department.dept_code})"


class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(5), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'),
                           nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey(
        'departments.id'), nullable=False)
    attendances = db.relationship('Attendance', backref='subject', lazy=True)

    def __repr__(self):
        return f"{self.name} ({self.subject_code})"


class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.Boolean, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey(
        'students.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey(
        'subjects.id'), nullable=False)

    def __repr__(self):
        return f"Subject({self.date}, {self.status}, {self.semester},\
                {self.student_id}, {self.subject_id})"
