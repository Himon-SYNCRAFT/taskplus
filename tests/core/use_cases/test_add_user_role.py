from unittest import mock

from taskplus.core.use_cases.add_user_role import AddUserRole
from taskplus.core.use_cases.add_user_role_request import AddUserRoleRequest


def test_add_user_role():
    role_name = 'admin'
    repo = mock.Mock()
    request = AddUserRoleRequest(name=role_name)

    use_case = AddUserRole(repo=repo)
    response = use_case.execute(request)

    assert bool(response) is True
    repo.save.assert_called_once()
    assert response.value.name == role_name
