from flask import Blueprint

recommender = Blueprint('recommender', __name__)

from . import routes, models
