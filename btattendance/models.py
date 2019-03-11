from btattendance import db
from werkzeug.security import generate_password_hash, check_password_hash


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    rollno = db.Column(db.Text)
    email = db.Column(db.Text)
    password_hash = db.Column(db.Text)
    macad = db.Column(db.Text)

    def __init__(self, name, rollno, email, password, macad):
        self.name = name
        self.rollno = rollno
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.macad = macad

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    password_hash = db.Column(db.Text)
    course = db.Column(db.Text)

    def __init__(self, name, email, password, course):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.course = course

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
