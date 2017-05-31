import json
from unittest import mock

from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.domain import UserRole


role_name = 'admin'
role = UserRole(name=role_name, id=1)
roles = [role]


@mock.patch('taskplus.apps.rest.routes.ListUserRolesAction')
def test_get_roles_list(mock_action, client):
    response = ResponseSuccess(roles)
    mock_action().execute.return_value = response

    http_response = client.get('/roles')

    assert json.loads(http_response.data.decode('UTF-8')) == [{
        'name': role.name,
        'id': role.id
    }]
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.GetRoleDetailsAction')
def test_get_role_details(mock_action, client):
    response = ResponseSuccess(role)
    mock_action().execute.return_value = response

    http_response = client.get('/role/{}'.format(role.id))

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': role.name,
        'id': role.id
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.AddUserRoleAction')
def test_add_role(mock_action, client):
    response = ResponseSuccess(role)
    mock_action().execute.return_value = response

    data = json.dumps(dict(name=role.name))
    http_response = client.post('/role', data=data,
                                content_type='application/json')

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': role.name,
        'id': role.id
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.DeleteUserRoleAction')
def test_delete_role(mock_action, client):
    response = ResponseSuccess(role)
    mock_action().execute.return_value = response

    http_response = client.delete('/role/{}'.format(role.id))

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': role.name,
        'id': role.id
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.UpdateUserRoleAction')
def test_update_role(mock_action, client):
    response = ResponseSuccess(role)
    mock_action().execute.return_value = response
    data = json.dumps(dict(id=role.id, name=role.name))

    http_response = client.put('/role', data=data,
                               content_type='application/json')

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': role.name,
        'id': role.id
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'