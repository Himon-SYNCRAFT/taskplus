import pytest
from unittest import mock

from taskplus.core.shared.response import ResponseFailure
from taskplus.core.actions import UpdateTaskAction, UpdateTaskRequest


def test_update_task_request():
    request = UpdateTaskRequest(id=1, name='name', content='content')

    assert request.id == 1
    assert request.name == 'name'
    assert request.content == 'content'


def test_update_task_request_without_data():
    with pytest.raises(TypeError):
        UpdateTaskRequest()


def test_update_task_request_without_id():
    request = UpdateTaskRequest(id=None)

    assert request.is_valid() is False
    assert any([e.parameter == 'id' and e.message == 'is required'
                for e in request.errors])
    assert len(request.errors) == 1


def test_update_task_request_invalid_data():
    request = UpdateTaskRequest(id=1, name=[], content=[])

    assert request.is_valid() is False
    assert len(request.errors) == 2
    print(request.errors)
    assert any(
        e.parameter == 'name' and e.message == 'expected str, got list([])'
        for e in request.errors
    )
    assert any(
        e.parameter == 'content' and e.message == 'expected str, got list([])'
        for e in request.errors
    )


def test_update_task():
    task_id = 1
    repo = mock.Mock()
    request = UpdateTaskRequest(id=task_id, name='name', content='content')
    action = UpdateTaskAction(tasks_repository=repo)
    response = action.execute(request)

    assert bool(response) is True
    assert repo.update.called
    assert response.value == repo.update.return_value


def test_update_task_with_hooks():
    task_id = 1
    repo = mock.Mock()
    request = UpdateTaskRequest(id=task_id, name='name', content='content')
    action = UpdateTaskAction(tasks_repository=repo)
    response = action.execute(request)

    before = mock.MagicMock()
    after = mock.MagicMock()

    action.add_before_execution_hook(before)
    action.add_after_execution_hook(after)

    response = action.execute(request)

    assert before.called
    assert after.called

    assert bool(response) is True
    assert repo.update.called
    assert response.value == repo.update.return_value


def test_update_task_handles_bad_request():
    repo = mock.Mock()
    request = UpdateTaskRequest(id=None, name=[], content=[])
    action = UpdateTaskAction(tasks_repository=repo)
    response = action.execute(request)

    assert bool(response) is False
    assert not repo.update.called
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': 'id: is required\nname: expected str, got list([])\ncontent: expected str, got list([])'
    }


def test_update_task_handle_generic_error():
    repo = mock.Mock()
    error_message = 'Just an error message'
    repo.update.side_effect = Exception(error_message)

    action = UpdateTaskAction(tasks_repository=repo)
    request = UpdateTaskRequest(id=2)
    response = action.execute(request)

    assert bool(response) is False
    assert repo.update.called
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }
