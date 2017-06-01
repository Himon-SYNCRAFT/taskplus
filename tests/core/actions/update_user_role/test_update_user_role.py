from unittest import mock

from taskplus.core.shared.response import ResponseFailure
from taskplus.core.actions import UpdateUserRoleAction
from taskplus.core.actions import UpdateUserRoleRequest


def test_update_user_role():
    user_role_id = 1
    repo = mock.Mock()
    request = UpdateUserRoleRequest(id=user_role_id, name='admin')
    action = UpdateUserRoleAction(repo=repo)
    response = action.execute(request)

    assert bool(response) is True
    assert repo.update.called
    assert response.value == repo.one.return_value


def test_update_user_role_handles_bad_request():
    repo = mock.Mock()
    request = UpdateUserRoleRequest(id=None, name=[])
    action = UpdateUserRoleAction(repo=repo)
    response = action.execute(request)

    assert bool(response) is False
    assert not repo.update.called
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': 'id: is required\nname: expected string, got list([])'
    }


def test_update_user_handle_generic_error():
    repo = mock.Mock()
    error_message = 'Just an error message'
    repo.update.side_effect = Exception(error_message)

    action = UpdateUserRoleAction(repo=repo)
    request = UpdateUserRoleRequest(id=2)
    response = action.execute(request)

    assert bool(response) is False
    assert repo.update.called
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }
