from flask import Flask, redirect, render_template, url_for
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(config)


# DB Config
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Login Configuration
login = LoginManager(app)
login.login_view = 'auth.loginUser'
login.message = 'Please Login To Access The Page'
login.login_message_category = 'info'
