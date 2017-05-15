import json
from unittest import mock

from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.domain import UserRole


role_name = 'admin'
role = UserRole(name=role_name)
roles = [role]


@mock.patch('taskplus.apps.rest.routes.ListUserRolesAction')
def test_get(mock_action, client):
    response = ResponseSuccess(roles)
    mock_action().execute.return_value = response

    http_response = client.get('/roles')

    assert json.loads(http_response.data.decode('UTF-8')) == [{'name': role.name}]
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'
