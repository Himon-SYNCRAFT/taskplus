from taskplus.core.actions import ListTaskStatusesRequest


def test_list_user_roles_request_without_parameters():
    request = ListTaskStatusesRequest()

    assert request.filters is None
    assert request.is_valid() is True


def test_list_user_roles_request_with_empty_filters():
    request = ListTaskStatusesRequest(filters={})

    assert request.filters is None
    assert request.is_valid() is True


def test_list_user_roles_request_with_filters():
    request = ListTaskStatusesRequest(filters={'a': 1, 'b': 2})

    assert request.filters == {'a': 1, 'b': 2}
    assert request.is_valid() is True


def test_list_user_roles_request_invalid_filters():
    request = ListTaskStatusesRequest(filters=5)

    assert request.is_valid() is False
    assert request.errors[0].parameter == 'filters'
