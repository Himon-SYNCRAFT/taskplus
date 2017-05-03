import json
from unittest import mock

from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.domain.user_role import UserRole


role_dict = dict(name='admin')
role = UserRole.from_dict(role_dict)
roles = [role]


@mock.patch('taskplus.apps.rest.routes.ListUserRoles')
def test_get(mock_use_case, client):
    response = ResponseSuccess(roles)
    print(response.value)
    mock_use_case().execute.return_value = response

    http_response = client.get('/roles')

    assert json.loads(http_response.data.decode('UTF-8')) == [role_dict]
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'
