import os
from flask import Flask
from flask_cors import CORS, cross_origin

from taskplus.apps.rest import routes
from taskplus.apps.rest.settings import ProdConfig, DevConfig, TestConfig
from taskplus.apps.rest.database import create_db
from taskplus.apps.rest.auth import login_manager, user_loader, request_loader,\
                                    unauthorized_handler


if os.environ.get('TESTING'):
    config = TestConfig
elif os.environ.get('PRODUCTION'):
    config = ProdConfig
else:
    config = DevConfig


def create_app(config_object=config):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.register_blueprint(routes.blueprint)

    login_manager.init_app(app)
    CORS(app, supports_credentials=True)
    # create_db()
    return app
