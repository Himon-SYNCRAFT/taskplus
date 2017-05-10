import pytest

from taskplus.core.actions import UpdateUserRequest


def test_update_user_request():
    request = UpdateUserRequest(id=1, name='abc')
    assert request.is_valid()
    assert request.id == 1
    assert request.name == 'abc'


def test_update_user_request_without_id():
    with pytest.raises(Exception):
        UpdateUserRequest()


def test_update_user_request_without_data():
    request = UpdateUserRequest(id=None)

    assert not request.is_valid()
    assert len(request.errors) == 1
    error = request.errors[0]
    assert error.parameter == 'id'
    assert error.message == 'is required'


def test_update_user_bad_request():
    request = UpdateUserRequest(id='ac', name=[], role_id='sdfs')

    assert not request.is_valid()
    assert len(request.errors) == 3
    assert any([e.parameter == 'id' and e.message == 'expected int, got str(ac)'
                for e in request.errors])
    assert any([e.parameter == 'name' and e.message == 'expected str, got list([])'
                for e in request.errors])
    assert any([
        e.parameter == 'role_id' and e.message == 'expected int, got str(sdfs)'
        for e in request.errors])
