import pytest
from unittest import mock

from taskplus.core.actions import ListTaskStatusesAction
from taskplus.core.actions import ListTaskStatusesRequest
from taskplus.core.domain import TaskStatus
from taskplus.core.shared.response import ResponseFailure


@pytest.fixture
def statuses():
    status1 = TaskStatus(name='new')
    status2 = TaskStatus(name='canceled')
    status3 = TaskStatus(name='completed')
    return [status1, status2, status3]


def test_list_statuses_without_parameters(statuses):
    repo = mock.Mock()
    repo.list.return_value = statuses

    request = ListTaskStatusesRequest()
    action = ListTaskStatusesAction(repo)

    response = action.execute(request)

    assert bool(response) is True
    repo.list.assert_called_with(filters=None)
    assert response.value == statuses


def test_list_statuses_with_parameters(statuses):
    repo = mock.Mock()
    repo.list.return_value = statuses
    status_name = 'new'
    filters = dict(name=status_name)

    request = ListTaskStatusesRequest(filters)
    action = ListTaskStatusesAction(repo)

    response = action.execute(request)

    assert bool(response) is True
    repo.list.assert_called_with(filters=filters)
    assert response.value == statuses


def test_list_statuses_handles_generic_error():
    repo = mock.Mock()
    error_message = 'Just an error message'
    repo.list.side_effect = Exception(error_message)

    request = ListTaskStatusesRequest()
    action = ListTaskStatusesAction(repo)

    response = action.execute(request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }


def test_list_statuses_handles_bad_request():
    repo = mock.Mock()

    request = ListTaskStatusesRequest(5)
    action = ListTaskStatusesAction(repo)

    response = action.execute(request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': 'filters: is not iterable'
    }
