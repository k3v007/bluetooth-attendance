from btattendance import db
from werkzeug.security import generate_password_hash, check_password_hash


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    rollno = db.Column(db.String(7), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    bd_addr = db.Column(db.Text, nullable=False, unique=True)

    def __init__(self, name, rollno, email, password, bd_addr):
        self.name = name
        self.rollno = rollno
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.bd_addr = bd_addr

    def __repr__(self):
        return f"Student('{self.name}', '{self.rollno}', '{self.email}', '{self.bd_addr}')" # noqa

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f"Teacher('{self.name}', '{self.email}')" # noqa

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
