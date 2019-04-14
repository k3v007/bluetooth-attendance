import os

from dotenv import load_dotenv
load_dotenv('.env')

from flask import Flask     # noqa
from flask_admin import Admin   # noqa
from flask_login import LoginManager    # noqa
from flask_mail import Mail     # noqa
from flask_sqlalchemy import SQLAlchemy     # noqa
from flask_rq2 import RQ    # noqa


admin = Admin()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
rq = RQ()


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    admin.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    rq.init_app(app)

    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'warning'

    from app.users.views import users
    from app.users.admin.views import administrator
    from app.users.students.views import students
    from app.users.teachers.views import teachers
    app.register_blueprint(users)
    app.register_blueprint(administrator, url_prefix='/admin')
    app.register_blueprint(students, url_prefix='/student')
    app.register_blueprint(teachers, url_prefix='/teacher')

    return app
