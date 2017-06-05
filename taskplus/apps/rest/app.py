from flask import Flask
from flask_login import LoginManager

from taskplus.apps.rest import routes
from taskplus.apps.rest.settings import DevConfig
from taskplus.apps.rest.database import create_db


login_manager = LoginManager()


def create_app(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.register_blueprint(routes.blueprint)

    login_manager.init_app(app)
    # create_db()
    return app
