from unittest import mock

from taskplus.core.actions import AddUserAction, AddUserRequest
from taskplus.core.domain import User, UserRole
from taskplus.core.shared.response import ResponseFailure


def test_add_user_action():
    name = 'name'
    password = 'password'
    role_id = 1

    roles_repo = mock.Mock()
    roles_repo.one.return_value = UserRole(name='role_name')

    users_repo = mock.Mock()
    users_repo.save.return_value = User(
        name=name, roles=[roles_repo.one.return_value])

    request = AddUserRequest(name=name, password=password, roles=[role_id])
    action = AddUserAction(users_repo, roles_repo)

    response = action.execute(request)

    assert users_repo.save.called
    assert bool(response) is True
    assert response.value == users_repo.save.return_value


def test_add_user_action_with_hooks():
    name = 'name'
    password = 'password'
    role_id = 1

    roles_repo = mock.Mock()
    roles_repo.one.return_value = UserRole(name='role_name')

    users_repo = mock.Mock()
    users_repo.save.return_value = User(
        name=name, roles=[roles_repo.one.return_value])

    request = AddUserRequest(name=name, password=password, roles=[role_id])
    action = AddUserAction(users_repo, roles_repo)

    before = mock.MagicMock()
    after = mock.MagicMock()

    action.add_before_execution_hook(before)
    action.add_after_execution_hook(after)

    response = action.execute(request)

    assert before.called
    assert after.called
    assert users_repo.save.called
    assert bool(response) is True
    assert response.value == users_repo.save.return_value


def test_add_user_action_handles_bad_request():
    name = None
    password = None
    role_id = None

    roles_repo = mock.Mock()
    roles_repo.one.return_value = UserRole(name='role_name')

    users_repo = mock.Mock()
    users_repo.save.return_value = User(
        name='name', roles=[roles_repo.one.return_value])

    request = AddUserRequest(name=name, password=password, roles=role_id)
    action = AddUserAction(users_repo, roles_repo)

    response = action.execute(request)

    assert not users_repo.save.called
    assert bool(response) is False
    assert response.value == {
        'message': 'name: is required\npassword: is required\nroles: is required',
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
