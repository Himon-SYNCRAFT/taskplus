from unittest import mock

from taskplus.core.actions import UpdateUserAction, UpdateUserRequest
from taskplus.core.domain import User
from taskplus.core.shared.response import ResponseFailure


def test_update_user_action():
    id, name = 1, 'name'
    users_repo = mock.Mock()
    users_repo.update.return_value = User(id=id, name=name, role=mock.Mock())

    request = UpdateUserRequest(id=id, name=name)

    action = UpdateUserAction(repo=users_repo)
    response = action.execute(request)

    assert bool(response) is True
    assert users_repo.update.called
    assert response.value == users_repo.update.return_value


def test_update_user_action_handles_bad_requst():
    name = 'name'
    users_repo = mock.Mock()
    users_repo.update.return_value = User(id=id, name=name, role=mock.Mock())

    request = UpdateUserRequest(id=None)

    action = UpdateUserAction(repo=users_repo)
    response = action.execute(request)

    assert bool(response) is False
    assert not users_repo.update.called
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': 'id: is required'
    }


def test_update_action_handles_exception():
    error_message = 'Error!!!'
    users_repo = mock.Mock()
    users_repo.update.side_effect = Exception(error_message)

    request = UpdateUserRequest(id=1)

    action = UpdateUserAction(repo=users_repo)
    response = action.execute(request)

    assert bool(response) is False
    assert users_repo.update.called
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }
