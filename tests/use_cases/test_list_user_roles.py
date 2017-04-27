import pytest
from unittest import mock

from taskplus.domain.user_role import UserRole
from taskplus.use_cases.list_user_roles import ListUserRoles
from taskplus.use_cases.list_user_roles_request import ListUserRolesRequest


@pytest.fixture
def roles():
    role1 = UserRole(name='admin')
    role2 = UserRole(name='doer')
    role3 = UserRole(name='creator')
    return [role1, role2, role3]


def test_list_roles_without_parameters(roles):
    repo = mock.Mock()
    repo.list.return_value = roles

    request = ListUserRolesRequest.from_dict({})
    use_case = ListUserRoles(repo)

    response = use_case.execute(request)

    assert bool(response) is True
    repo.list.assert_called_with()
    assert response.value == roles
