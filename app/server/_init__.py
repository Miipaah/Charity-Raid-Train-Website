from flask import Blueprint

server = Blueprint('server', __name__)

from . import routes, webhooks
# Import other modules like error handlers, utilities, etc.