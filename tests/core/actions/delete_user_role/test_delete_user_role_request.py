from taskplus.core.actions import DeleteUserRoleRequest


def test_delete_user_role_request():
    user_role_id = 1
    request = DeleteUserRoleRequest(id=user_role_id)

    assert request.is_valid() is True
    assert request.id == user_role_id


def test_delete_user_role_request_without_id():
    request = DeleteUserRoleRequest(id=None)

    assert request.is_valid() is False
    assert request.id is None
