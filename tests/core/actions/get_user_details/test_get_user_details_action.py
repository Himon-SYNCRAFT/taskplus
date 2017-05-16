from unittest import mock

from taskplus.core.actions import GetUserDetailsAction, GetUserDetailsRequest
from taskplus.core.domain import User
from taskplus.core.shared.response import ResponseFailure


def test_get_user_details_action():
    role = mock.Mock()
    user = User(name='admin', id=1, role=role)
    users_repo = mock.Mock()
    users_repo.get.return_value = user
    request = GetUserDetailsRequest(user.id)

    action = GetUserDetailsAction(users_repo)
    response = action.execute(request)

    assert bool(response) is True
    users_repo.get.assert_called_once_with(user.id)
    assert response.value == user


def test_get_user_details_action_handles_bad_request():
    role = mock.Mock()
    user = User(name='admin', id=1, role=role)
    users_repo = mock.Mock()
    users_repo.get.return_value = user
    request = GetUserDetailsRequest(user_id=None)

    action = GetUserDetailsAction(users_repo)
    response = action.execute(request)

    assert bool(response) is False
    assert not users_repo.get.called
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': 'user_id: is required'
    }


def test_get_user_details_action_handles_generic_error():
    error_message = 'Error!!!'
    users_repo = mock.Mock()
    users_repo.get.side_effect = Exception(error_message)
    request = GetUserDetailsRequest(user_id=1)

    action = GetUserDetailsAction(users_repo)
    response = action.execute(request)

    assert bool(response) is False
    users_repo.get.assert_called_once_with(1)
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }
