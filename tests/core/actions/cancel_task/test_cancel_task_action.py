from unittest import mock

from taskplus.core.shared.response import ResponseFailure
from taskplus.core.actions import CancelTaskAction, CancelTaskRequest


def test_cancel_task_action():
    task_repo = mock.Mock()
    status_repo = mock.Mock()
    action = CancelTaskAction(task_repo=task_repo, status_repo=status_repo)
    request = CancelTaskRequest(task_id=1)
    response = action.execute(request)

    assert bool(response) is True
    assert task_repo.update.called


def test_cancel_task_action_handles_bad_request():
    task_repo = mock.Mock()
    status_repo = mock.Mock()
    action = CancelTaskAction(task_repo=task_repo, status_repo=status_repo)
    request = CancelTaskRequest(task_id=None)
    response = action.execute(request)

    assert bool(response) is False
    assert not task_repo.update.called
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': 'task_id: is required'
    }


def test_cancel_task_action_handles_generic_error():
    error_message = 'Error!!!'
    task_repo = mock.Mock()
    task_repo.update.side_effect = Exception(error_message)
    status_repo = mock.Mock()
    action = CancelTaskAction(task_repo=task_repo, status_repo=status_repo)
    request = CancelTaskRequest(task_id=1)
    response = action.execute(request)

    assert bool(response) is False
    assert task_repo.update.called
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }
