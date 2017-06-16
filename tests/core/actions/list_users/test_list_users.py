from unittest import mock
import pytest

from taskplus.core.actions import ListUsersAction, ListUsersRequest
from taskplus.core.domain import User
from taskplus.core.shared.response import ResponseFailure


@pytest.fixture
def users():
    return [
        User('name1', roles=mock.Mock()),
        User('name2', roles=mock.Mock()),
    ]


def test_list_users_action_without_parameters(users):
    repo = mock.Mock()
    repo.list.return_value = users
    request = ListUsersRequest()
    action = ListUsersAction(repo=repo)
    response = action.execute(request)

    assert bool(response) is True
    assert response.value == repo.list.return_value


def test_list_users_action_with_hooks(users):
    repo = mock.Mock()
    repo.list.return_value = users
    request = ListUsersRequest()
    action = ListUsersAction(repo=repo)

    before = mock.MagicMock()
    after = mock.MagicMock()

    action.add_before_execution_hook(before)
    action.add_after_execution_hook(after)

    response = action.execute(request)

    assert before.called
    assert after.called

    assert bool(response) is True
    assert response.value == repo.list.return_value


def test_list_users_action_with_parameters(users):
    filters = dict(name='name1')
    repo = mock.Mock()
    repo.list.return_value = [u for u in users if u.name == filters['name']]
    request = ListUsersRequest(filters=filters)
    action = ListUsersAction(repo=repo)
    response = action.execute(request)

    assert bool(response) is True
    assert response.value == repo.list.return_value


def test_list_handles_bad_request():
    repo = mock.Mock()
    request = ListUsersRequest(filters=5)
    action = ListUsersAction(repo=repo)
    response = action.execute(request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': 'filters: is not iterable'
    }


def test_list_handles_exception():
    repo = mock.Mock()
    error_message = 'Error!!!'
    repo.list.side_effect = Exception(error_message)
    request = ListUsersRequest()
    action = ListUsersAction(repo=repo)
    response = action.execute(request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }
