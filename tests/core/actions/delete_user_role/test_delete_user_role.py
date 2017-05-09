from unittest import mock

from taskplus.core.actions import DeleteUserRoleAction
from taskplus.core.actions import DeleteUserRoleRequest


def test_delete_user_role():
    user_role_id = 1
    request = DeleteUserRoleRequest(id=user_role_id)
    repo = mock.Mock()
    repo.delete.return_value = user_role_id

    action = DeleteUserRoleAction(repo=repo)
    response = action.execute(request)

    repo.delete.assert_called_once()
    assert bool(response) is True
    assert response.value == repo.delete.return_value
