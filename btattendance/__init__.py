from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from btattendance.config import Config


app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)
Migrate(app, db)

from btattendance.students.views import students # noqa
from btattendance.teachers.views import teachers # noqa

app.register_blueprint(students)
app.register_blueprint(teachers)
