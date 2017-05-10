from taskplus.core.actions import ListUsersRequest


def test_list_users_request_without_parameters():
    request = ListUsersRequest()
    assert request.is_valid() is True
    assert request.filters is None


def test_list_users_request_with_filters():
    filters = dict(name='user')
    request = ListUsersRequest(filters=filters)
    assert request.is_valid() is True
    assert request.filters == filters


def test_list_users_request_with_empty_filters():
    filters = {}
    request = ListUsersRequest(filters=filters)
    assert request.is_valid() is True
    assert request.filters is None


def test_list_users_request_invalid_filters():
    filters = 5
    request = ListUsersRequest(filters=filters)

    assert request.is_valid() is False
    assert request.filters == filters
    assert len(request.errors) == 1
    error = request.errors[0]
    assert error.parameter == 'filters'
    assert error.message == 'is not iterable'
