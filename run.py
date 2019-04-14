from flask import render_template

from app import create_app, db
from app.models import Department
from app.utils import load_departments


flask_app = create_app()


@flask_app.before_first_request
def insert_dept():
    # Check if table already exists or not
    if db.session.query(Department).first() is None:
        departments = load_departments()
        for dept in departments:
            db.session.add(Department(**dept))
        db.session.commit()


# Home
@flask_app.route('/')
@flask_app.route('/home')
def index():
    return render_template('home.html')


# About
@flask_app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    flask_app.run()
