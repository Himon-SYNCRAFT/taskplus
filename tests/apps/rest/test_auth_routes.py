import json
from unittest import mock

from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.domain import User, UserRole


user_name = 'admin'
user = User(name=user_name, id=1, role=UserRole(id=1, name='creator'))
users = [user]


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
        'role': {
            'id': user.role.id,
            'name': user.role.name,
        }
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
