from unittest import mock

from taskplus.core.actions import AddUserRoleAction
from taskplus.core.actions import AddUserRoleRequest


def test_add_user_role():
    role_name = 'admin'
    repo = mock.Mock()
    request = AddUserRoleRequest(name=role_name)

    action = AddUserRoleAction(repo=repo)
    response = action.execute(request)

    assert bool(response) is True
    repo.save.assert_called_once()
    assert response.value.name == role_name
