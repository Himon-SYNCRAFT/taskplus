import pytest
from unittest import mock

from taskplus.core.domain.user_role import UserRole
from taskplus.core.use_cases.list_user_roles import ListUserRoles
from taskplus.core.use_cases.list_user_roles_request import ListUserRolesRequest
from taskplus.core.shared.response import ResponseFailure


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
    repo.list.assert_called_with(filters=None)
    assert response.value == roles


def test_list_roles_with_parameters(roles):
    repo = mock.Mock()
    repo.list.return_value = roles
    role_name = 'creator'
    filters = dict(name=role_name)

    request = ListUserRolesRequest.from_dict({'filters': filters})
    use_case = ListUserRoles(repo)

    response = use_case.execute(request)

    assert bool(response) is True
    repo.list.assert_called_with(filters=filters)
    assert response.value == roles


def test_list_roles_handles_generic_error():
    repo = mock.Mock()
    error_message = 'Just an error message'
    repo.list.side_effect = Exception(error_message)

    request = ListUserRolesRequest.from_dict({})
    use_case = ListUserRoles(repo)

    response = use_case.execute(request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }


def test_list_roles_handles_bad_request():
    repo = mock.Mock()

    request = ListUserRolesRequest.from_dict({'filters': 5})
    use_case = ListUserRoles(repo)

    response = use_case.execute(request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': 'filters: Is not iterable'
    }
