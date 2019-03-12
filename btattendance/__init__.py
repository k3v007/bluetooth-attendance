from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from btattendance.config import Config


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from btattendance.students.views import students # noqa
    from btattendance.teachers.views import teachers # noqa
    app.register_blueprint(students, url_prefix='/student')
    app.register_blueprint(teachers, url_prefix='/teacher')

    return app
