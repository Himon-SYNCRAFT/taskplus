from taskplus.use_cases.list_user_roles_request import ListUserRolesRequest


def test_list_user_roles_request_without_parameters():
    request = ListUserRolesRequest()

    assert request.filters is None
    assert bool(request) is True


def test_list_user_roles_request_from_empty_dict():
    request = ListUserRolesRequest.from_dict({})

    assert request.filters is None
    assert bool(request) is True


def test_list_user_roles_request_with_empty_filters():
    request = ListUserRolesRequest(filters={})

    assert request.filters == {}
    assert bool(request) is True


def test_list_user_roles_request_from_dict_with_empty_filters():
    request = ListUserRolesRequest.from_dict({'filters': {}})

    assert request.filters == {}
    assert bool(request) is True


def test_list_user_roles_request_with_filters():
    request = ListUserRolesRequest(filters={'a': 1, 'b': 2})

    assert request.filters == {'a': 1, 'b': 2}
    assert bool(request) is True


def test_list_user_roles_request_from_dict_with_filters():
    request = ListUserRolesRequest.from_dict({'filters': {'a': 1, 'b': 2}})

    assert request.filters == {'a': 1, 'b': 2}
    assert bool(request) is True


def test_list_user_roles_request_invalid_filters():
    request = ListUserRolesRequest.from_dict({'filters': 5})

    assert request.has_errors()
    assert request._errors[0].parameter == 'filters'
    assert bool(request) is False
