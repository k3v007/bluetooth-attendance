from btattendance import create_app
from flask import render_template

app = create_app()

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
    app.run()
