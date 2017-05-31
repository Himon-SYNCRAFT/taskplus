from unittest import mock
import pytest

from taskplus.core.actions import GetNotCompletedTasksAction,\
     GetNotCompletedTasksRequest
from taskplus.core.domain import Task
from taskplus.core.shared.response import ResponseFailure


@pytest.fixture
def tasks():
    return [
        Task(name='name1', content=[], status=mock.Mock(), creator=mock.Mock()),
        Task(name='name2', content=[], status=mock.Mock(), creator=mock.Mock()),
    ]


def test_get_not_completed_tasks(tasks):
    repo = mock.Mock()
    repo.list.return_value = tasks
    request = GetNotCompletedTasksRequest()
    action = GetNotCompletedTasksAction(task_repo=repo)
    response = action.execute(request)

    assert bool(response) is True
    assert response.value == repo.list.return_value


def test_list_handles_exception():
    repo = mock.Mock()
    error_message = 'Error!!!'
    repo.list.side_effect = Exception(error_message)
    request = GetNotCompletedTasksRequest()
    action = GetNotCompletedTasksAction(task_repo=repo)
    response = action.execute(request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }
