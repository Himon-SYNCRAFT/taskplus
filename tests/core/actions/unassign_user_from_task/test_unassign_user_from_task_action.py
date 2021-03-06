from unittest import mock

from taskplus.core.actions import (UnassignUserFromTaskAction,
                                   UnassignUserFromTaskRequest)
from taskplus.core.shared.response import ResponseFailure


def test_unassign_user_from_task_action():
    tasks_repo = mock.Mock()
    request = UnassignUserFromTaskRequest(task_id=1)

    action = UnassignUserFromTaskAction(tasks_repo=tasks_repo)
    response = action.execute(request)

    assert bool(response) is True
    assert tasks_repo.update.called


def test_unassign_user_from_task_action_with_hooks():
    tasks_repo = mock.Mock()
    request = UnassignUserFromTaskRequest(task_id=1)

    action = UnassignUserFromTaskAction(tasks_repo=tasks_repo)

    before = mock.MagicMock()
    after = mock.MagicMock()

    action.add_before_execution_hook(before)
    action.add_after_execution_hook(after)

    response = action.execute(request)

    assert before.called
    assert after.called

    assert bool(response) is True
    assert tasks_repo.update.called


def test_unassign_user_from_task_action_handles_bad_request():
    tasks_repo = mock.Mock()
    request = UnassignUserFromTaskRequest(task_id=None)

    action = UnassignUserFromTaskAction(tasks_repo=tasks_repo)
    response = action.execute(request)

    assert bool(response) is False
    assert not tasks_repo.update.called
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': 'task_id: is required'
    }


def test_unassign_user_from_task_action_handles_generic_error():
    error_message = 'Error1!!'
    tasks_repo = mock.Mock()
    tasks_repo.update.side_effect = Exception(error_message)
    request = UnassignUserFromTaskRequest(task_id=1)

    action = UnassignUserFromTaskAction(tasks_repo=tasks_repo)
    response = action.execute(request)

    assert bool(response) is False
    assert tasks_repo.update.called
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }
