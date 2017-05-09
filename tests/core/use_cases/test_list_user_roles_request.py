from taskplus.core.use_cases.list_user_roles_request import\
     ListUserRolesRequest


def test_list_user_roles_request_without_parameters():
    request = ListUserRolesRequest()
    print(request.errors)

    assert request.filters is None
    assert request.is_valid() is True


def test_list_user_roles_request_with_empty_filters():
    request = ListUserRolesRequest(filters={})

    assert request.filters is None
    assert request.is_valid() is True


def test_list_user_roles_request_with_filters():
    request = ListUserRolesRequest(filters={'a': 1, 'b': 2})

    assert request.filters == {'a': 1, 'b': 2}
    assert request.is_valid() is True


def test_list_user_roles_request_invalid_filters():
    request = ListUserRolesRequest(filters=5)

    assert request.is_valid() is False
    assert request.errors[0].parameter == 'filters'
