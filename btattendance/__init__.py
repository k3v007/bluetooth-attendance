from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'vks1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root1234@localhost/btDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

from btattendance.students.views import students # noqa
from btattendance.teachers.views import teachers # noqa

app.register_blueprint(students)
app.register_blueprint(teachers)
