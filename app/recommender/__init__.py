from flask import Blueprint

recommender = Blueprint('recommender', __name__, template_folder='templates')

from . import routes, models
