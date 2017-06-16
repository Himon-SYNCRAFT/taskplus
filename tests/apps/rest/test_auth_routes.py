import json
from unittest import mock
from sqlalchemy import event
from sqlalchemy.engine import Engine
from collections import namedtuple

from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.domain import User, UserRole
from taskplus.apps.rest.database import Base, db_session, engine


user_name = 'admin'
user = User(name=user_name, id=1, roles=[UserRole(id=1, name='creator')])
users = [user]


def setup_function(function):
    user_ = namedtuple('user_', ['id', 'name', 'role_id', 'role_name'])
    creator_ = user_(id=1, name='creator', role_id=1, role_name='creator_role')
    doer_ = user_(id=2, name='doer', role_id=2, role_name='doer_role')

    if db_session.bind.driver == 'pysqlite':
        @event.listens_for(Engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    with mock.patch('taskplus.apps.rest.models.User._hash_password',
                    side_effect=lambda x: x):
        from taskplus.apps.rest import models
        Base.metadata.reflect(engine)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        creator_role = models.UserRole(name=creator_.role_name,
                                       id=creator_.role_id)
        doer_role = models.UserRole(name=doer_.role_name,
                                    id=doer_.role_id)

        db_session.add(creator_role)
        db_session.add(doer_role)
        db_session.commit()

        creator = models.User(name=creator_.name, roles=[creator_role],
                              id=creator_.id, password='pass')
        doer = models.User(name=doer_.name, roles=[doer_role],
                           id=doer_.id, password='pass')

        db_session.add(creator)
        db_session.add(doer)
        db_session.commit()


@mock.patch('taskplus.apps.rest.routes.users_repository.check_password',
            side_effect=lambda _, __: True)
@mock.patch('taskplus.apps.rest.routes.ListUsersAction')
def test_login(mock_action, repo, client):
    response = ResponseSuccess(users)
    mock_action().execute.return_value = response

    data = json.dumps(dict(name=user.name, password='password'))
    http_response = client.post('/auth/login', data=data,
                                content_type='application/json')

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': user.name,
        'id': user.id,
        'roles': [{
            'id': user.roles[0].id,
            'name': user.roles[0].name,
        }]
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.users_repository.check_password',
            side_effect=lambda _, __: True)
@mock.patch('taskplus.apps.rest.routes.ListUsersAction')
def test_login_invalid_name(mock_action, repo, client):
    response = ResponseSuccess([])
    mock_action().execute.return_value = response

    data = json.dumps(dict(name=user.name, password='password'))
    http_response = client.post('/auth/login', data=data,
                                content_type='application/json')

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'message': 'Login failed. User with name {} not found.'.format(
            user.name)
    }
    assert http_response.status_code == 401
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.users_repository.check_password',
            side_effect=lambda _, __: False)
@mock.patch('taskplus.apps.rest.routes.ListUsersAction')
def test_login_invalid_password(mock_action, repo, client):
    response = ResponseSuccess(users)
    mock_action().execute.return_value = response

    data = json.dumps(dict(name=user.name, password='password'))
    http_response = client.post('/auth/login', data=data,
                                content_type='application/json')

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'message': 'Login failed. Invalid password.'
    }
    assert http_response.status_code == 401
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.users_repository.check_password',
            side_effect=lambda _, __: True)
@mock.patch('taskplus.apps.rest.routes.ListUsersAction')
def test_logout(mock_action, repo, client):
    response = ResponseSuccess(users)
    mock_action().execute.return_value = response

    data = json.dumps(dict(name=user.name, password='password'))
    client.post('/auth/login', data=data, content_type='application/json')

    http_response = client.get('/auth/logout', content_type='application/json')

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'message': 'Logged out'
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'
