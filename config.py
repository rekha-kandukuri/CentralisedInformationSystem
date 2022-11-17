import os
basedir = os.path.abspath(os.path.dirname(__file__))

class config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '334nadnj&&89Ydau89YAd98adbszmdi3*&&923kln'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+os.getcwd()+'/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    ADMINS = ['kandukurirekha14@gmail.com']