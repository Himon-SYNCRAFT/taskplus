import json
from sqlalchemy import event
from sqlalchemy.engine import Engine

from taskplus.apps.rest.database import Base, db_session, engine
from taskplus.apps.rest.repositories import UsersRepository
from taskplus.apps.rest.routes import authorization_manager
from taskplus.core.domain import Statuses


users_repository = UsersRepository()


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

    status_new = models.TaskStatus(id=Statuses.NEW, name='new')
    status_in_progress = models.TaskStatus(
        id=Statuses.IN_PROGRESS, name='in progress')
    status_completed = models.TaskStatus(
        id=Statuses.COMPLETED, name='completed')
    status_canceled = models.TaskStatus(
        id=Statuses.CANCELED, name='canceled')

    db_session.add(status_new)
    db_session.add(status_in_progress)
    db_session.add(status_completed)
    db_session.add(status_canceled)
    db_session.commit()

    user = users_repository.one(3)
    authorization_manager.user = user


def test_get_statuses_list(client):
    http_response = client.get('/statuses')

    assert json.loads(http_response.data.decode('UTF-8')) == [
        {'name': 'new', 'id': 1},
        {'name': 'in progress', 'id': 2},
        {'name': 'completed', 'id': 3},
        {'name': 'canceled', 'id': 4},
    ]
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_get_statuses_list_with_filters(client):
    name = 'new'
    data = json.dumps(dict(filters=dict(name=name)))
    http_response = client.post('/statuses', data=data,
                                content_type='application/json')

    assert json.loads(http_response.data.decode('UTF-8')) == [{
        'name': name,
        'id': 1
    }]
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_get_status_details(client):
    id = 1
    name = 'new'
    http_response = client.get('/status/{}'.format(id))

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': name,
        'id': id
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_add_status(client):
    id = 5
    name = 'status_name'
    data = json.dumps(dict(name=name))
    http_response = client.post('/status', data=data,
                                content_type='application/json')

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': name,
        'id': id
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_delete_status(client):
    id = 1
    name = 'new'
    http_response = client.delete('/status/{}'.format(id))

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': name,
        'id': id
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_update_status(client):
    id = 1
    name = 'status_name'
    data = json.dumps(dict(name=name))

    http_response = client.put('/status/{}'.format(id), data=data,
                               content_type='application/json')

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': name,
        'id': id
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'
