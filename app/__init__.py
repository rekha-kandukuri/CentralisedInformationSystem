from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO, send


# general configs
app = Flask(__name__)
app.config.from_object(config)
socketio = SocketIO(app, engineio_logger=True, logger=True)


# DB Configs
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Login Configs
login = LoginManager(app)
login.login_view = 'auth.loginUser'
login.message = 'Please Login To Access The Page'
login.login_message_category = 'info'


# Blueprint Registrations
from app.auth import auth
from app.course import course
from app.recommender import recommender
from app.forum import forum
from app.home import home

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(course, url_prefix='/course')
app.register_blueprint(recommender, url_prefix='/recommender')
app.register_blueprint(forum, url_prefix='/forum')
app.register_blueprint(home, url_prefix='')

from .utils import errorhandlers
from .admin import Admin
from .mailconfig import mail
