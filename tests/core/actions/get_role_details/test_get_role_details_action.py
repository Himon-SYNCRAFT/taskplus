from unittest import mock

from taskplus.core.actions import GetRoleDetailsAction, GetRoleDetailsRequest
from taskplus.core.domain import UserRole
from taskplus.core.shared.response import ResponseFailure


def test_get_role_details_action():
    role = mock.Mock()
    role = UserRole(name='admin', id=1)
    roles_repo = mock.Mock()
    roles_repo.one.return_value = role
    request = GetRoleDetailsRequest(role.id)

    action = GetRoleDetailsAction(roles_repo)
    response = action.execute(request)

    assert bool(response) is True
    roles_repo.one.assert_called_once_with(role.id)
    assert response.value == role


def test_get_role_details_action_handles_bad_request():
    role = mock.Mock()
    role = UserRole(name='admin', id=1)
    roles_repo = mock.Mock()
    roles_repo.one.return_value = role
    request = GetRoleDetailsRequest(role_id=None)

    action = GetRoleDetailsAction(roles_repo)
    response = action.execute(request)

    assert bool(response) is False
    assert not roles_repo.one.called
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': 'role_id: is required'
    }


def test_get_role_details_action_handles_generic_error():
    error_message = 'Error!!!'
    roles_repo = mock.Mock()
    roles_repo.one.side_effect = Exception(error_message)
    request = GetRoleDetailsRequest(role_id=1)

    action = GetRoleDetailsAction(roles_repo)
    response = action.execute(request)

    assert bool(response) is False
    roles_repo.one.assert_called_once_with(1)
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }
