from flask import Blueprint

bp = Blueprint('interface', __name__, url_prefix='/interface')

from . import routes, models