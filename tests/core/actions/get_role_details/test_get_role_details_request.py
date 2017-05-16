from taskplus.core.actions import GetRoleDetailsRequest


def test_get_role_details_request():
    role_id = 1
    request = GetRoleDetailsRequest(role_id)

    assert request.is_valid()
    assert request.role_id == role_id


def test_get_role_details_request_without_id():
    role_id = None
    request = GetRoleDetailsRequest(role_id)

    assert not request.is_valid()
    assert request.role_id == role_id
    assert len(request.errors) == 1
    error = request.errors[0]
    assert error.parameter == 'role_id'
    assert error.message == 'is required'


def test_get_role_details_bad_request():
    role_id = 'asd'
    request = GetRoleDetailsRequest(role_id)

    assert not request.is_valid()
    assert request.role_id == role_id
    assert len(request.errors) == 1
    error = request.errors[0]
    assert error.parameter == 'role_id'
    assert error.message == 'expected int, got str(asd)'
