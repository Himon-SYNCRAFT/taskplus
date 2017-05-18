import pytest
from taskplus.core.actions import AddUserRoleRequest


new_role_name = 'admin'


def test_add_user_role_request_init():
    request = AddUserRoleRequest(name=new_role_name)

    assert request.name == new_role_name
    assert request.is_valid()


def test_add_user_role_request_without_data():
    with pytest.raises(Exception):
        AddUserRoleRequest()


def test_add_user_role_request_name_is_none():
    name = None
    request = AddUserRoleRequest(name)

    assert request.name == name
    assert not request.is_valid()
    assert any(
        [e.parameter == 'name' and e.message == 'is required'
            for e in request.errors]
    )


def test_add_user_role_request_name_is_empty_string():
    name = ''
    request = AddUserRoleRequest(name)

    assert request.name == name
    assert not request.is_valid()
    assert any(
        [e.parameter == 'name' and e.message == 'is required'
            for e in request.errors]
    )


def test_add_user_role_request_invalid_data():
    request = AddUserRoleRequest(name=5)

    assert request.name == 5
    assert not request.is_valid()
    assert any(
        [e.parameter == 'name' and e.message == 'expected string, got int(5)'
            for e in request.errors]
    )
