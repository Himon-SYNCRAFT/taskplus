from unittest import mock

from taskplus.core.actions import (GetTaskStatusDetailsAction,
                                   GetTaskStatusDetailsRequest)
from taskplus.core.domain import TaskStatus
from taskplus.core.shared.response import ResponseFailure


def test_get_status_details_action():
    status = mock.Mock()
    status = TaskStatus(name='new', id=1)
    statuses_repo = mock.Mock()
    statuses_repo.one.return_value = status
    request = GetTaskStatusDetailsRequest(status.id)

    action = GetTaskStatusDetailsAction(statuses_repo)
    response = action.execute(request)

    assert bool(response) is True
    statuses_repo.one.assert_called_once_with(status.id)
    assert response.value == status


def test_get_status_details_action_with_hooks():
    status = mock.Mock()
    status = TaskStatus(name='new', id=1)
    statuses_repo = mock.Mock()
    statuses_repo.one.return_value = status
    request = GetTaskStatusDetailsRequest(status.id)

    action = GetTaskStatusDetailsAction(statuses_repo)

    before = mock.MagicMock()
    after = mock.MagicMock()

    action.add_before_execution_hook(before)
    action.add_after_execution_hook(after)

    response = action.execute(request)

    assert before.called
    assert after.called

    assert bool(response) is True
    statuses_repo.one.assert_called_once_with(status.id)
    assert response.value == status


def test_get_status_details_action_handles_bad_request():
    status = mock.Mock()
    status = TaskStatus(name='new', id=1)
    statuses_repo = mock.Mock()
    statuses_repo.one.return_value = status
    request = GetTaskStatusDetailsRequest(status_id=None)

    action = GetTaskStatusDetailsAction(statuses_repo)
    response = action.execute(request)

    assert bool(response) is False
    assert not statuses_repo.one.called
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': 'status_id: is required'
    }


def test_get_status_details_action_handles_generic_error():
    error_message = 'Error!!!'
    statuses_repo = mock.Mock()
    statuses_repo.one.side_effect = Exception(error_message)
    request = GetTaskStatusDetailsRequest(status_id=1)

    action = GetTaskStatusDetailsAction(statuses_repo)
    response = action.execute(request)

    assert bool(response) is False
    statuses_repo.one.assert_called_once_with(1)
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }


def test_get_status_details_request():
    status_id = 1
    request = GetTaskStatusDetailsRequest(status_id)

    assert request.is_valid()
    assert request.status_id == status_id


def test_get_status_details_request_without_id():
    status_id = None
    request = GetTaskStatusDetailsRequest(status_id)

    assert not request.is_valid()
    assert request.status_id == status_id
    assert len(request.errors) == 1
    error = request.errors[0]
    assert error.parameter == 'status_id'
    assert error.message == 'is required'


def test_get_status_details_bad_request():
    status_id = 'asd'
    request = GetTaskStatusDetailsRequest(status_id)

    assert not request.is_valid()
    assert request.status_id == status_id
    assert len(request.errors) == 1
    error = request.errors[0]
    assert error.parameter == 'status_id'
    assert error.message == 'expected int, got str(asd)'
