import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root1234@localhost/btDB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
