from unittest import mock

from taskplus.core.use_cases.delete_user_role import DeleteUserRole
from taskplus.core.use_cases.delete_user_role_request import DeleteUserRoleRequest


def test_delete_user_role():
    user_role_id = 1
    request = DeleteUserRoleRequest(id=user_role_id)
    repo = mock.Mock()
    repo.delete.return_value = user_role_id

    use_case = DeleteUserRole(repo=repo)
    response = use_case.execute(request)

    repo.delete.assert_called_once()
    assert bool(response) is True
    assert response.value == repo.delete.return_value
