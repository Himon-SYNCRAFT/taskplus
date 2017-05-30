from unittest import mock

from taskplus.core.actions import GetTaskDetailsAction, GetTaskDetailsRequest
from taskplus.core.domain import Task
from taskplus.core.shared.response import ResponseFailure


def test_get_task_details_action():
    creator = mock.Mock()
    status = mock.Mock()
    task = Task(name='task', content=[], status=status, creator=creator, id=1)
    tasks_repo = mock.Mock()
    tasks_repo.one.return_value = task
    request = GetTaskDetailsRequest(task.id)

    action = GetTaskDetailsAction(tasks_repo)
    response = action.execute(request)

    assert bool(response) is True
    tasks_repo.one.assert_called_once_with(task.id)
    assert response.value == task


def test_get_task_details_action_handles_bad_request():
    creator = mock.Mock()
    status = mock.Mock()
    task = Task(name='task', content=[], status=status, creator=creator, id=1)
    tasks_repo = mock.Mock()
    tasks_repo.one.return_value = task
    request = GetTaskDetailsRequest(task_id=None)

    action = GetTaskDetailsAction(tasks_repo)
    response = action.execute(request)

    assert bool(response) is False
    assert not tasks_repo.one.called
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': 'task_id: is required'
    }


def test_get_task_details_action_handles_generic_error():
    error_message = 'Error!!!'
    tasks_repo = mock.Mock()
    tasks_repo.one.side_effect = Exception(error_message)
    request = GetTaskDetailsRequest(task_id=1)

    action = GetTaskDetailsAction(tasks_repo)
    response = action.execute(request)

    assert bool(response) is False
    tasks_repo.one.assert_called_once_with(1)
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }
