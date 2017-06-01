from unittest import mock

from taskplus.core.actions import AddUserRoleAction, AddUserRoleRequest
from taskplus.core.shared.response import ResponseFailure


def test_add_user_role_action():
    role_name = 'admin'
    roles_repo = mock.Mock()
    roles_repo.save.return_value = mock.Mock()
    request = AddUserRoleRequest(name=role_name)

    action = AddUserRoleAction(roles_repo)
    response = action.execute(request)

    assert bool(response) is True
    assert roles_repo.save.called
    assert response.value == roles_repo.save.return_value


def test_add_user_role_action_handles_bad_request():
    role_name = None
    roles_repo = mock.Mock()

    request = AddUserRoleRequest(name=role_name)
    action = AddUserRoleAction(roles_repo)
    response = action.execute(request)

    assert bool(response) is False
    assert not roles_repo.save.called
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': 'name: is required'
    }


def test_add_user_role_action_handles_generic_error():
    error_message = 'error'
    role_name = 'admin'
    roles_repo = mock.Mock()
    roles_repo.save.side_effect = Exception(error_message)

    request = AddUserRoleRequest(name=role_name)
    action = AddUserRoleAction(roles_repo)
    response = action.execute(request)

    assert bool(response) is False
    assert roles_repo.save.called
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }
