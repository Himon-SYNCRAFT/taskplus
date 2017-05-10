from taskplus.core.actions import DeleteUserRequest


def test_delete_user_request():
    request = DeleteUserRequest(id=1)

    assert request.id == 1
    assert request.is_valid()


def test_delete_user_request_without_id():
    request = DeleteUserRequest(id=None)

    assert request.id is None
    assert not request.is_valid()
    assert len(request.errors) == 1
    error = request.errors[0]
    assert error.parameter == 'id'
    assert error.message == 'is required'


def test_delete_user_bad_request():
    invalid_id = [1, 2, 3]
    request = DeleteUserRequest(id=invalid_id)

    assert request.id == invalid_id
    assert not request.is_valid()
    assert len(request.errors) == 1
    error = request.errors[0]
    assert error.parameter == 'id'
    assert error.message == 'expected int, got {}({})'.format(
        invalid_id.__class__.__name__, invalid_id)
