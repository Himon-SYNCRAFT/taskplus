from unittest import mock

from taskplus.core.shared.response import ResponseFailure
from taskplus.core.actions import AssignUserToTaskAction, AssignUserToTaskRequest


def test_assign_user_to_task_action():
    tasks_repo = mock.Mock()
    users_repo = mock.Mock()

    request = AssignUserToTaskRequest(task_id=1, user_id=2)

    action = AssignUserToTaskAction(tasks_repo, users_repo)
    response = action.execute(request)

    assert bool(response) is True
    tasks_repo.update.assert_called_once()


def test_assing_user_to_task_action_handles_bad_request():
    tasks_repo = mock.Mock()
    users_repo = mock.Mock()

    request = AssignUserToTaskRequest(task_id=None, user_id=None)

    action = AssignUserToTaskAction(tasks_repo, users_repo)
    response = action.execute(request)

    assert bool(response) is False
    assert not tasks_repo.update.called
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': 'task_id: is required\nuser_id: is required'
    }


def test_assign_user_to_task_action_handles_generic_error():
    error_message = 'Error!!!'
    tasks_repo = mock.Mock()
    tasks_repo.update.side_effect = Exception(error_message)
    users_repo = mock.Mock()

    request = AssignUserToTaskRequest(task_id=1, user_id=2)

    action = AssignUserToTaskAction(tasks_repo, users_repo)
    response = action.execute(request)

    assert bool(response) is False
    tasks_repo.update.assert_called_once()
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }
