from flask import Flask

from taskplus.apps.rest import routes
from taskplus.apps.rest.settings import DevConfig
from taskplus.apps.rest.database import create_db
from taskplus.apps.rest.auth import login_manager, user_loader, request_loader,\
                                    unauthorized_handler


def create_app(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.register_blueprint(routes.blueprint)

    login_manager.init_app(app)
    # create_db()
    return app
