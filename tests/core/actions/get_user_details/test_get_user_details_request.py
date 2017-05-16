from taskplus.core.actions import GetUserDetailsRequest


def test_get_user_details_request():
    user_id = 1
    request = GetUserDetailsRequest(user_id)

    assert request.is_valid()
    assert request.user_id == user_id


def test_get_user_details_request_without_id():
    user_id = None
    request = GetUserDetailsRequest(user_id)

    assert not request.is_valid()
    assert request.user_id == user_id
    assert len(request.errors) == 1
    error = request.errors[0]
    assert error.parameter == 'user_id'
    assert error.message == 'is required'


def test_get_user_details_bad_request():
    user_id = 'asd'
    request = GetUserDetailsRequest(user_id)

    assert not request.is_valid()
    assert request.user_id == user_id
    assert len(request.errors) == 1
    error = request.errors[0]
    assert error.parameter == 'user_id'
    assert error.message == 'expected int, got str(asd)'
