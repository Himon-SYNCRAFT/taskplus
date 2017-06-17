import json
from sqlalchemy import event
from sqlalchemy.engine import Engine

from taskplus.apps.rest.repositories import UsersRepository
from taskplus.apps.rest.routes import authorization_manager
from taskplus.apps.rest.database import Base, db_session, engine


user_repository = UsersRepository()


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

    creator_role = models.UserRole(name='creator')
    doer_role = models.UserRole(name='doer')
    admin_role = models.UserRole(name='admin')
    unused_role = models.UserRole(name='dummy')

    db_session.add(creator_role)
    db_session.add(doer_role)
    db_session.add(admin_role)
    db_session.add(unused_role)
    db_session.commit()

    creator = models.User(name='creator', roles=[creator_role],
                          password='creator')
    doer = models.User(name='doer', roles=[doer_role], password='doer')
    super_user = models.User(
        name='super',
        roles=[creator_role, doer_role, admin_role],
        password='super'
    )

    db_session.add(creator)
    db_session.add(doer)
    db_session.add(super_user)
    db_session.commit()

    user = user_repository.one(3)
    authorization_manager.user = user


def test_get_roles_list(client):
    http_response = client.get('/roles')

    assert json.loads(http_response.data.decode('UTF-8')) == [
        {'name': 'creator', 'id': 1},
        {'name': 'doer', 'id': 2},
        {'name': 'admin', 'id': 3},
        {'name': 'dummy', 'id': 4},
    ]
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_get_roles_list_with_filters(client):
    filters = json.dumps(dict(filters=dict(name='creator')))
    http_response = client.post('/roles', data=filters,
                                content_type='application/json')

    assert json.loads(http_response.data.decode('UTF-8')) == [{
        'name': 'creator',
        'id': 1
    }]
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_get_role_details(client):
    http_response = client.get('/role/{}'.format(1))

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': 'creator',
        'id': 1
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_add_role(client):
    role_name = 'role_name'
    data = json.dumps(dict(name=role_name))
    http_response = client.post('/role', data=data,
                                content_type='application/json')

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': role_name,
        'id': 5
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_delete_role(client):
    role_id = 4
    http_response = client.delete('/role/{}'.format(role_id))

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': 'dummy',
        'id': role_id
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_update_role(client):
    role_name = 'role_name'
    data = json.dumps(dict(name=role_name))

    http_response = client.put('/role/1', data=data,
                               content_type='application/json')

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': role_name,
        'id': 1
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'
