from unittest import mock

from taskplus.core.actions import AddTaskAction, AddTaskRequest
from taskplus.core.domain import Task
from taskplus.core.shared.response import ResponseFailure


def test_add_task_action():
    task_name = 'task_name'
    task_content = 'task_content'
    creator_id = 1
    task_id = 1

    users_repo = mock.Mock()
    tasks_repo = mock.Mock()
    statuses_repo = mock.Mock()

    tasks_repo.save.return_value = Task(name=task_name, content=task_content,
                                        status=mock.Mock(), creator=mock.Mock(),
                                        doer=None, id=task_id)

    request = AddTaskRequest(name=task_name, creator_id=creator_id,
                             content=task_content)
    action = AddTaskAction(tasks_repo, users_repo, statuses_repo)
    response = action.execute(request)

    assert bool(response) is True
    assert tasks_repo.save.called
    assert response.value == tasks_repo.save.return_value


def test_add_task_action_with_hooks():
    task_name = 'task_name'
    task_content = 'task_content'
    creator_id = 1
    task_id = 1

    users_repo = mock.Mock()
    tasks_repo = mock.Mock()
    statuses_repo = mock.Mock()

    tasks_repo.save.return_value = Task(name=task_name, content=task_content,
                                        status=mock.Mock(), creator=mock.Mock(),
                                        doer=None, id=task_id)

    request = AddTaskRequest(name=task_name, creator_id=creator_id,
                             content=task_content)
    action = AddTaskAction(tasks_repo, users_repo, statuses_repo)

    before = mock.MagicMock()
    after = mock.MagicMock()
    action.add_before_execution_hook(before)
    action.add_after_execution_hook(after)

    response = action.execute(request)

    assert before.called
    assert after.called
    assert bool(response) is True
    assert tasks_repo.save.called
    assert response.value == tasks_repo.save.return_value


def test_add_task_action_handles_bad_request():
    task_name = ''
    task_content = ''
    creator_id = None

    users_repo = mock.Mock()
    tasks_repo = mock.Mock()
    statuses_repo = mock.Mock()

    request = AddTaskRequest(name=task_name, creator_id=creator_id,
                             content=task_content)
    action = AddTaskAction(tasks_repo, users_repo, statuses_repo)
    response = action.execute(request)

    assert not tasks_repo.save.called
    assert bool(response) is False
    message = 'name: is required\ncontent: is required\ncreator_id: is required'
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': message
    }


def test_add_task_action_handles_generic_error():
    error_message = 'Error'

    users_repo = mock.Mock()
    statuses_repo = mock.Mock()
    tasks_repo = mock.Mock()
    tasks_repo.save.side_effect = Exception(error_message)

    request = mock.Mock()
    request.is_valid.return_value = True
    action = AddTaskAction(tasks_repo, users_repo, statuses_repo)
    response = action.execute(request)

    assert tasks_repo.save.called
    assert bool(response) is False
    message = 'Exception: {}'.format(error_message)
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': message
    }
