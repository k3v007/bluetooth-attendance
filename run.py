from flask import render_template

from btattendance import create_app, db
from btattendance.models import Department

app = create_app()


# @app.before_first_request
# def createDept():
#     d1 = Department('coe', 'A K Sharma', 'aks@gmail.com')
#     d2 = Department('it', 'V S Prasad', 'vsp@gmail.com')
#     d3 = Department('ece', 'Manoj Khanna', 'manoj@gmail.com')
#     d4 = Department('ice', 'Savita S.', 'savita@gmail.com')
#     d5 = Department('me', 'Kavita M.', 'kavita@gmail.com')
#     d6 = Department('bt', 'Sunil Vohra', 'sunil@gmail.com')
#     try:    
#         db.session.add_all([d1, d2, d3, d4, d5, d6])
#         db.session.commit()
#     except:
#         print("Data already exists!")


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
