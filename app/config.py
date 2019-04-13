import os


class Config:
    # App settings
    DEBUG = False
    TESTING = True
    SECRET_KEY = os.environ['SECRET_KEY']
    # Main Settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ['EMAIL_USER']
    MAIL_PASSWORD = os.environ['EMAIL_PASS']
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Redis Settings
    RQ_REDIS_URL = os.environ['REDIS_URL']


class Dev(Config):
    DEBUG = True
    TESTING = False
    MAIL_SUPPRESS_SEND = False
