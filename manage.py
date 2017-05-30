from flask_script import Manager, Server
from flask_script.commands import Clean, ShowUrls

from taskplus.apps.rest.app import create_app
from taskplus.apps.rest.database import create_db


app = create_app()


@app.route('/')
def hello():
    return 'hello'


manager = Manager(app)

manager.add_command('server', Server())
manager.add_command('ulrs', ShowUrls())
manager.add_command('clean', Clean())


if __name__ == '__main__':
    create_db()
    manager.run()
