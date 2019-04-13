from flask import render_template

from app import create_app


flask_app = create_app()


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
