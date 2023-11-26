from flask import Flask
from flask import Flask

from app.api import sheets_api, tiltify_api, fourthwall_api
from app.server import webhooks
from app.server import server as server_blueprint

app = Flask(__name__)
app.register_blueprint(server_blueprint, url_prefix='/server')

