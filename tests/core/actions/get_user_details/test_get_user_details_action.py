from unittest import mock

from taskplus.core.actions import GetUserDetailsAction, GetUserDetailsRequest
from taskplus.core.domain import User
from taskplus.core.shared.response import ResponseFailure


def test_get_user_details_action():
    roles = mock.Mock()
    user = User(name='admin', id=1, roles=roles)
    users_repo = mock.Mock()
    users_repo.one.return_value = user
    request = GetUserDetailsRequest(user.id)

    action = GetUserDetailsAction(users_repo)
    response = action.execute(request)

    assert bool(response) is True
    users_repo.one.assert_called_once_with(user.id)
    assert response.value == user


def test_get_user_details_action_with_hooks():
    roles = mock.Mock()
    user = User(name='admin', id=1, roles=roles)
    users_repo = mock.Mock()
    users_repo.one.return_value = user
    request = GetUserDetailsRequest(user.id)

    action = GetUserDetailsAction(users_repo)

    before = mock.MagicMock()
    after = mock.MagicMock()

    action.add_before_execution_hook(before)
    action.add_after_execution_hook(after)

    response = action.execute(request)

    assert before.called
    assert after.called

    assert bool(response) is True
    users_repo.one.assert_called_once_with(user.id)
    assert response.value == user


def test_get_user_details_action_handles_bad_request():
    roles = mock.Mock()
    user = User(name='admin', id=1, roles=roles)
    users_repo = mock.Mock()
    users_repo.one.return_value = user
    request = GetUserDetailsRequest(user_id=None)

    action = GetUserDetailsAction(users_repo)
    response = action.execute(request)

    assert bool(response) is False
    assert not users_repo.one.called
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': 'user_id: is required'
    }


def test_get_user_details_action_handles_generic_error():
    error_message = 'Error!!!'
    users_repo = mock.Mock()
    users_repo.one.side_effect = Exception(error_message)
    request = GetUserDetailsRequest(user_id=1)

    action = GetUserDetailsAction(users_repo)
    response = action.execute(request)

    assert bool(response) is False
    users_repo.one.assert_called_once_with(1)
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }
