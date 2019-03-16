from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from btattendance.config import Config
from flask_mail import Mail
from flask_migrate import Migrate


db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.login_view = 'students.login'
    login_manager.login_message_category = 'warning'

    from btattendance.students.views import students  # noqa
    from btattendance.teachers.views import teachers  # noqa
    app.register_blueprint(students, url_prefix='/student')
    app.register_blueprint(teachers, url_prefix='/teacher')

    return app
