from taskplus.core.use_cases.add_user_role_request import AddUserRoleRequest


new_role_name = 'admin'


def test_add_valid_user_role():
    request = AddUserRoleRequest(name=new_role_name)

    assert request.name == new_role_name
    assert bool(request) is True


def test_add_valid_user_role_from_dict():
    data = dict(name=new_role_name)
    request = AddUserRoleRequest.from_dict(data)

    assert request.name == new_role_name
    assert bool(request) is True
