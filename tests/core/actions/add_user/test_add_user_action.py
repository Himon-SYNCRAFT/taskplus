from unittest import mock

from taskplus.core.actions import AddUserAction, AddUserRequest
from taskplus.core.domain import User, UserRole
from taskplus.core.shared.response import ResponseFailure


def test_add_user_action():
    name = 'name'
    role_id = 1

    roles_repo = mock.Mock()
    roles_repo.get.return_value = UserRole(name='role_name')

    users_repo = mock.Mock()
    users_repo.save.return_value = User(name, roles_repo.get.return_value)

    request = AddUserRequest(name=name, role_id=role_id)
    action = AddUserAction(users_repo, roles_repo)

    response = action.execute(request)

    users_repo.save.assert_called_once()
    assert bool(response) is True
    assert response.value == users_repo.save.return_value


def test_add_user_action_handles_bad_request():
    name = None
    role_id = None

    roles_repo = mock.Mock()
    roles_repo.get.return_value = UserRole(name='role_name')

    users_repo = mock.Mock()
    users_repo.save.return_value = User('name', roles_repo.get.return_value)

    request = AddUserRequest(name=name, role_id=role_id)
    action = AddUserAction(users_repo, roles_repo)

    response = action.execute(request)

    assert not users_repo.save.called
    assert bool(response) is False
    assert response.value == {
        'message': 'name: is required\nrole_id: is required',
        'type': ResponseFailure.PARAMETER_ERROR
    }


def test_add_user_action_handles_generic_error():
    error_message = 'Just an error message'
    users_repo = mock.Mock()
    users_repo.save.side_effect = Exception(error_message)

    roles_repo = mock.Mock()

    request = mock.Mock()
    request.is_valid.return_value = True

    action = AddUserAction(users_repo=users_repo, roles_repo=roles_repo)
    response = action.execute(request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }
