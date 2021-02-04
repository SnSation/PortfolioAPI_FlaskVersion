from flask import Blueprint

bp = Blueprint('v3', __name__, url_prefix='/v3')

from . import routes, models