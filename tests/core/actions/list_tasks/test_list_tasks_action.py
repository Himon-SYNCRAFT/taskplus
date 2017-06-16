from unittest import mock
import pytest

from taskplus.core.actions import ListTasksAction, ListTasksRequest
from taskplus.core.domain import Task
from taskplus.core.shared.response import ResponseFailure


@pytest.fixture
def tasks():
    return [
        Task(name='name1', content=[], status=mock.Mock(), creator=mock.Mock()),
        Task(name='name2', content=[], status=mock.Mock(), creator=mock.Mock()),
    ]


def test_list_tasks_action_without_parameters(tasks):
    repo = mock.Mock()
    repo.list.return_value = tasks
    request = ListTasksRequest()
    action = ListTasksAction(repo=repo)
    response = action.execute(request)

    assert bool(response) is True
    assert response.value == repo.list.return_value


def test_list_tasks_action_with_hooks(tasks):
    repo = mock.Mock()
    repo.list.return_value = tasks
    request = ListTasksRequest()
    action = ListTasksAction(repo=repo)

    before = mock.MagicMock()
    after = mock.MagicMock()

    action.add_before_execution_hook(before)
    action.add_after_execution_hook(after)

    response = action.execute(request)

    assert before.called
    assert after.called

    assert bool(response) is True
    assert response.value == repo.list.return_value


def test_list_tasks_action_with_parameters(tasks):
    filters = dict(name='name1')
    repo = mock.Mock()
    repo.list.return_value = [u for u in tasks if u.name == filters['name']]
    request = ListTasksRequest(filters=filters)
    action = ListTasksAction(repo=repo)
    response = action.execute(request)

    assert bool(response) is True
    assert response.value == repo.list.return_value


def test_list_handles_bad_request():
    repo = mock.Mock()
    request = ListTasksRequest(filters=5)
    action = ListTasksAction(repo=repo)
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
    request = ListTasksRequest()
    action = ListTasksAction(repo=repo)
    response = action.execute(request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }
