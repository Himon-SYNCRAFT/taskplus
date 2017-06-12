import json
from unittest import mock

from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.domain import User, UserRole


user_name = 'admin'
user = User(name=user_name, id=1, roles=[UserRole(id=1, name='creator')])
users = [user]


@mock.patch('taskplus.apps.rest.routes.ListUsersAction')
def test_get_users_list(mock_action, client):
    response = ResponseSuccess(users)
    mock_action().execute.return_value = response

    http_response = client.get('/users')
    roles = [{'id': role.id, 'name': role.name} for role in user.roles]

    assert json.loads(http_response.data.decode('UTF-8')) == [{
        'name': user.name,
        'id': user.id,
        'roles': roles
    }]
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.ListUsersAction')
def test_get_users_list_with_filters(mock_action, client):
    response = ResponseSuccess(users)
    mock_action().execute.return_value = response

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


@mock.patch('taskplus.apps.rest.routes.GetUserDetailsAction')
def test_get_user_details(mock_action, client):
    response = ResponseSuccess(user)
    mock_action().execute.return_value = response

    http_response = client.get('/user/{}'.format(user.id))
    roles = [{'id': role.id, 'name': role.name} for role in user.roles]

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': user.name,
        'id': user.id,
        'roles': roles
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.AddUserAction')
def test_add_user(mock_action, client):
    response = ResponseSuccess(user)
    mock_action().execute.return_value = response

    data = json.dumps(dict(name=user.name, roles=[1], password='password'))
    http_response = client.post('/user', data=data,
                                content_type='application/json')
    roles = [{'id': role.id, 'name': role.name} for role in user.roles]

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': user.name,
        'id': user.id,
        'roles': roles
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.DeleteUserAction')
def test_delete_user(mock_action, client):
    response = ResponseSuccess(user)
    mock_action().execute.return_value = response

    http_response = client.delete('/user/{}'.format(user.id))
    roles = [{'id': role.id, 'name': role.name} for role in user.roles]

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': user.name,
        'id': user.id,
        'roles': roles
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.UpdateUserAction')
def test_update_user(mock_action, client):
    response = ResponseSuccess(user)
    mock_action().execute.return_value = response
    data = json.dumps(dict(id=user.id, name=user.name))

    http_response = client.put('/user', data=data,
                               content_type='application/json')
    roles = [{'id': role.id, 'name': role.name} for role in user.roles]

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': user.name,
        'id': user.id,
        'roles': roles
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'
