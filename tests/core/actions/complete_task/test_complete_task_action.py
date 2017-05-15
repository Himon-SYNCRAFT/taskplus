from unittest import mock

from taskplus.core.actions import CompleteTaskAction, CompleteTaskRequest
from taskplus.core.shared.response import ResponseFailure


def test_complete_task_action():
    task_id = 1
    task_repo = mock.Mock()
    status_repo = mock.Mock()

    action = CompleteTaskAction(task_repo, status_repo)
    request = CompleteTaskRequest(task_id)
    response = action.execute(request)

    assert bool(response) is True
    task_repo.update.assert_called_once()


def test_complete_task_action_handles_bad_request():
    task_id = None
    task_repo = mock.Mock()
    status_repo = mock.Mock()

    action = CompleteTaskAction(task_repo, status_repo)
    request = CompleteTaskRequest(task_id)
    response = action.execute(request)

    assert bool(response) is False
    assert not task_repo.update.called
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': 'task_id: is required'
    }


def test_complete_task_action_handles_generic_error():
    error_message = 'Error!!!'
    task_id = 1
    task_repo = mock.Mock()
    task_repo.update.side_effect = Exception(error_message)
    status_repo = mock.Mock()

    action = CompleteTaskAction(task_repo, status_repo)
    request = CompleteTaskRequest(task_id)
    response = action.execute(request)

    assert bool(response) is False
    task_repo.update.assert_called_once()
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }
