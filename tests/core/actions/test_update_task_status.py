import pytest
from unittest import mock

from taskplus.core.shared.response import ResponseFailure
from taskplus.core.actions import UpdateTaskStatusAction, UpdateTaskStatusRequest


def test_update_task_status_request():
    request = UpdateTaskStatusRequest(id=1, name='new')

    assert request.id == 1
    assert request.name == 'new'
    assert request.is_valid() is True


def test_update_task_status_request_without_data():
    with pytest.raises(TypeError):
        UpdateTaskStatusRequest()


def test_update_task_status_request_without_id():
    request = UpdateTaskStatusRequest(id=None)

    assert request.is_valid() is False
    assert any([e.parameter == 'id' and e.message == 'is required'
                for e in request.errors])
    assert len(request.errors) == 1


def test_update_task_status_request_invalid_data():
    request = UpdateTaskStatusRequest(id=1, name=[])

    assert request.is_valid() is False
    message = 'expected string, got list([])'
    assert any([e.parameter == 'name' and e.message == message
                for e in request.errors])
    assert len(request.errors) == 1


def test_update_task_status():
    task_status_id = 1
    repo = mock.Mock()
    request = UpdateTaskStatusRequest(id=task_status_id, name='new')
    action = UpdateTaskStatusAction(repo=repo)
    response = action.execute(request)

    assert bool(response) is True
    repo.update.assert_called_once()
    assert response.value == repo.one.return_value


def test_update_task_status_handles_bad_request():
    repo = mock.Mock()
    request = UpdateTaskStatusRequest(id=None, name=[])
    action = UpdateTaskStatusAction(repo=repo)
    response = action.execute(request)

    assert bool(response) is False
    assert not repo.update.called
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': 'id: is required\nname: expected string, got list([])'
    }


def test_update_user_handle_generic_error():
    repo = mock.Mock()
    error_message = 'Just an error message'
    repo.update.side_effect = Exception(error_message)

    action = UpdateTaskStatusAction(repo=repo)
    request = UpdateTaskStatusRequest(id=2)
    response = action.execute(request)

    assert bool(response) is False
    repo.update.assert_called_once()
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }
