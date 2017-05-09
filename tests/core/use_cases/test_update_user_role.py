from unittest import mock

from taskplus.core.shared.response import ResponseFailure
from taskplus.core.use_cases.update_user_role import UpdateUserRole
from taskplus.core.use_cases.update_user_role_request import UpdateUserRoleRequest


def test_update_user_role():
    user_role_id = 1
    repo = mock.Mock()
    request = UpdateUserRoleRequest(id=user_role_id, name='admin')
    use_case = UpdateUserRole(repo=repo)
    response = use_case.execute(request)

    assert bool(response) is True
    repo.update.assert_called_once()
    assert response.value == repo.one.return_value


def test_update_user_role_handles_bad_request():
    repo = mock.Mock()
    request = UpdateUserRoleRequest(id=None, name=[])
    use_case = UpdateUserRole(repo=repo)
    response = use_case.execute(request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': 'id: is required\nname: expected string, got list([])'
    }


def test_update_user_handle_generic_error():
    repo = mock.Mock()
    error_message = 'Just an error message'
    repo.update.side_effect = Exception(error_message)

    use_case = UpdateUserRole(repo=repo)
    request = UpdateUserRoleRequest(id=2)
    response = use_case.execute(request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }
