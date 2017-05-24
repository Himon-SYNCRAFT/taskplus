from flask import Flask

from taskplus.apps.rest import routes
from taskplus.apps.rest.settings import DevConfig
from taskplus.apps.rest.database import create_db


def create_app(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.register_blueprint(routes.blueprint)
    create_db()
    return app
