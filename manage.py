from datetime import timedelta
from flask_script import Manager, Server
from flask_script.commands import Clean, ShowUrls
import flask
import flask_login

from taskplus.apps.rest.app import create_app
from taskplus.apps.rest.database import create_db


app = create_app()


@app.before_request
def before_request():
    flask.session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)
    flask.session.modified = True
    flask.g.user = flask_login.current_user


manager = Manager(app)

manager.add_command('server', Server())
manager.add_command('ulrs', ShowUrls())
manager.add_command('clean', Clean())


if __name__ == '__main__':
    create_db()
    manager.run()
