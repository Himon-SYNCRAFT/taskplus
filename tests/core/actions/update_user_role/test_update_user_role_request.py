import pytest

from taskplus.core.actions import UpdateUserRoleRequest


def test_update_user_role_request():
    request = UpdateUserRoleRequest(id=1, name='admin')

    assert request.id == 1
    assert request.name == 'admin'
    assert request.is_valid() is True


def test_update_user_role_request_without_data():
    with pytest.raises(TypeError):
        UpdateUserRoleRequest()


def test_update_user_role_request_without_id():
    request = UpdateUserRoleRequest(id=None)

    assert request.is_valid() is False
    assert any([e.parameter == 'id' and e.message == 'is required'
                for e in request.errors])
    assert len(request.errors) == 1


def test_update_user_role_request_invalid_data():
    request = UpdateUserRoleRequest(id=1, name=[])

    assert request.is_valid() is False
    message = 'expected string, got list([])'
    assert any([e.parameter == 'name' and e.message == message
                for e in request.errors])
    assert len(request.errors) == 1
