from taskplus.core.actions import ListTasksRequest


def test_list_tasks_request_without_parameters():
    request = ListTasksRequest()
    assert request.is_valid() is True
    assert request.filters is None


def test_list_tasks_request_with_filters():
    filters = dict(name='task')
    request = ListTasksRequest(filters=filters)
    assert request.is_valid() is True
    assert request.filters == filters


def test_list_tasks_request_with_empty_filters():
    filters = {}
    request = ListTasksRequest(filters=filters)
    assert request.is_valid() is True
    assert request.filters is None


def test_list_tasks_request_invalid_filters():
    filters = 5
    request = ListTasksRequest(filters=filters)

    assert request.is_valid() is False
    assert request.filters == filters
    assert len(request.errors) == 1
    error = request.errors[0]
    assert error.parameter == 'filters'
    assert error.message == 'is not iterable'
