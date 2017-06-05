from taskplus.core.actions import AddUserRequest


def test_add_user_request():
    role_id = 1
    name = 'name'
    password = 'password'
    request = AddUserRequest(name=name, password=password, role_id=role_id)

    assert request.is_valid() is True
    assert request.name == name
    assert request.role_id == role_id


def test_add_user_bad_request():
    role_id = 'abc'
    name = 1
    password = 1
    request = AddUserRequest(name=name, password=password, role_id=role_id)

    assert request.is_valid() is False
    assert len(request.errors) == 3
    errors = request.errors
    assert any([param == 'role_id' and message == "expected int, got str(abc)"
                for param, message in errors])
    assert any([param == 'name' and message == "expected str, got int(1)"
                for param, message in errors])
    assert any([param == 'password' and message == "expected str, got int(1)"
                for param, message in errors])


def test_add_user_request_without_data():
    request = AddUserRequest(name=None, password=None, role_id=None)

    assert request.is_valid() is False
    assert len(request.errors) == 3
    errors = request.errors
    assert any([param == 'role_id' and message == "is required"
                for param, message in errors])
    assert any([param == 'name' and message == "is required"
                for param, message in errors])
    assert any([param == 'password' and message == "is required"
                for param, message in errors])
