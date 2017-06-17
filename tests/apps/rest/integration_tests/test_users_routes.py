import json
from sqlalchemy import event
from sqlalchemy.engine import Engine
from collections import namedtuple

from taskplus.apps.rest.repositories import UsersRepository
from taskplus.apps.rest.routes import authorization_manager
from taskplus.apps.rest.database import Base, db_session, engine


users_repository = UsersRepository()

User = namedtuple('User', ['id', 'name', 'roles'])
Role = namedtuple('Role', ['id', 'name'])

user = User(id=1, name='super', roles=[
    Role(id=1, name='creator'),
    Role(id=2, name='doer'),
    Role(id=3, name='admin'),
])


def setup_function(function):
    if db_session.bind.driver == 'pysqlite':
        @event.listens_for(Engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    from taskplus.apps.rest import models
    Base.metadata.reflect(engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    roles = [models.UserRole(name=role.name, id=role.id) for role in user.roles]

    for role in roles:
        db_session.add(role)

    db_session.commit()

    db_session.add(models.User(
        id=user.id,
        name=user.name,
        roles=roles,
        password='super'
    ))

    db_session.commit()

    user_ = users_repository.one(1)
    authorization_manager.user = user_


def test_get_users_list(client):
    http_response = client.get('/users')
    roles = [dict(id=role.id, name=role.name) for role in user.roles]

    assert json.loads(http_response.data.decode('UTF-8')) == [
        {'id': user.id, 'name': user.name, 'roles': roles}
    ]
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_get_users_list_with_filters(client):
    data = json.dumps(dict(filters=dict(name=user.name)))
    http_response = client.post('/users', data=data,
                                content_type='application/json')
    roles = [{'id': role.id, 'name': role.name} for role in user.roles]

    assert json.loads(http_response.data.decode('UTF-8')) == [{
        'name': user.name,
        'id': user.id,
        'roles': roles
    }]
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_get_user_details(client):
    http_response = client.get('/user/{}'.format(user.id))
    roles = [{'id': role.id, 'name': role.name} for role in user.roles]

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': user.name,
        'id': user.id,
        'roles': roles
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_add_user(client):
    name = 'newuser'
    data = json.dumps(dict(
        name=name, roles=[role.id for role in user.roles], password='password'))
    http_response = client.post('/user', data=data,
                                content_type='application/json')
    roles = [{'id': role.id, 'name': role.name} for role in user.roles]

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': name,
        'id': 2,
        'roles': roles
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_delete_user(client):
    http_response = client.delete('/user/{}'.format(user.id))
    roles = [{'id': role.id, 'name': role.name} for role in user.roles]

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': user.name,
        'id': user.id,
        'roles': roles
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_update_user(client):
    data = json.dumps(dict(id=user.id, name='name'))

    http_response = client.put('/user', data=data,
                               content_type='application/json')
    roles = [{'id': role.id, 'name': role.name} for role in user.roles]

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': 'name',
        'id': user.id,
        'roles': roles
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'
