from btattendance import create_app
from flask import render_template
from flask_script import Manager
from flask_migrate import MigrateCommand

app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Home
@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
