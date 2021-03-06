import pytest
from unittest import mock

from taskplus.core.actions import ListUserRolesAction
from taskplus.core.actions import ListUserRolesRequest
from taskplus.core.domain import UserRole
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

    request = ListUserRolesRequest()
    action = ListUserRolesAction(repo)

    response = action.execute(request)

    assert bool(response) is True
    repo.list.assert_called_with(filters=None)
    assert response.value == roles


def test_list_roles_with_hooks(roles):
    repo = mock.Mock()
    repo.list.return_value = roles

    request = ListUserRolesRequest()
    action = ListUserRolesAction(repo)

    before = mock.MagicMock()
    after = mock.MagicMock()

    action.add_before_execution_hook(before)
    action.add_after_execution_hook(after)

    response = action.execute(request)

    assert before.called
    assert after.called

    assert bool(response) is True
    repo.list.assert_called_with(filters=None)
    assert response.value == roles


def test_list_roles_with_parameters(roles):
    repo = mock.Mock()
    repo.list.return_value = roles
    role_name = 'creator'
    filters = dict(name=role_name)

    request = ListUserRolesRequest(filters)
    action = ListUserRolesAction(repo)

    response = action.execute(request)

    assert bool(response) is True
    repo.list.assert_called_with(filters=filters)
    assert response.value == roles


def test_list_roles_handles_generic_error():
    repo = mock.Mock()
    error_message = 'Just an error message'
    repo.list.side_effect = Exception(error_message)

    request = ListUserRolesRequest()
    action = ListUserRolesAction(repo)

    response = action.execute(request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }


def test_list_roles_handles_bad_request():
    repo = mock.Mock()

    request = ListUserRolesRequest(5)
    action = ListUserRolesAction(repo)

    response = action.execute(request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': 'filters: Is not iterable'
    }
