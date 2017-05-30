import pytest
from unittest import mock

from taskplus.core.actions import AddTaskStatusAction, AddTaskStatusRequest
from taskplus.core.shared.response import ResponseFailure


new_status_name = 'new'


def test_add_task_status_request_init():
    request = AddTaskStatusRequest(name=new_status_name)

    assert request.name == new_status_name
    assert request.is_valid()


def test_add_task_status_request_without_data():
    with pytest.raises(Exception):
        AddTaskStatusRequest()


def test_add_task_status_request_name_is_none():
    name = None
    request = AddTaskStatusRequest(name)

    assert request.name == name
    assert not request.is_valid()
    assert any(
        [e.parameter == 'name' and e.message == 'is required'
            for e in request.errors]
    )


def test_add_task_status_request_name_is_empty_string():
    name = ''
    request = AddTaskStatusRequest(name)

    assert request.name == name
    assert not request.is_valid()
    assert any(
        [e.parameter == 'name' and e.message == 'is required'
            for e in request.errors]
    )


def test_add_task_status_request_invalid_data():
    request = AddTaskStatusRequest(name=5)

    assert request.name == 5
    assert not request.is_valid()
    assert any(
        [e.parameter == 'name' and e.message == 'expected string, got int(5)'
            for e in request.errors]
    )


def test_add_task_status_action():
    status_name = 'new'
    statuses_repo = mock.Mock()
    statuses_repo.save.return_value = mock.Mock()
    request = AddTaskStatusRequest(name=status_name)

    action = AddTaskStatusAction(statuses_repo)
    response = action.execute(request)

    assert bool(response) is True
    statuses_repo.save.assert_called_once()
    assert response.value == statuses_repo.save.return_value


def test_add_task_status_action_handles_bad_request():
    status_name = None
    statuses_repo = mock.Mock()

    request = AddTaskStatusRequest(name=status_name)
    action = AddTaskStatusAction(statuses_repo)
    response = action.execute(request)

    assert bool(response) is False
    assert not statuses_repo.save.called
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': 'name: is required'
    }


def test_add_task_status_action_handles_generic_error():
    error_message = 'error'
    status_name = new_status_name
    statuses_repo = mock.Mock()
    statuses_repo.save.side_effect = Exception(error_message)

    request = AddTaskStatusRequest(name=status_name)
    action = AddTaskStatusAction(statuses_repo)
    response = action.execute(request)

    assert bool(response) is False
    statuses_repo.save.assert_called_once()
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }
