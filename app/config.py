import os


class Config:
    # App settings
    DEBUG = False
    TESTING = True
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    # Main Settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ['EMAIL_USER']
    MAIL_PASSWORD = os.environ['EMAIL_PASS']
    FLASKY_MAIL_SENDER = 'noreply@bluetooth_attendance.com'
    # Database settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Redis Settings
    REDIS_URL = os.environ['REDIS_URL']


class Dev(Config):
    DEBUG = True
    TESTING = False
    MAIL_SUPPRESS_SEND = False
