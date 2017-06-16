from taskplus.core.domain import User, UserRole
from taskplus.core.authorization import Permission


def test_user():
    name = 'name'
    permissions = [Permission('AddUserAction')]
    roles = [UserRole(name='role_name'), UserRole(name="role_name2")]
    user = User(name=name, roles=roles, permissions=permissions)

    assert user.name == name
    assert user.roles == roles
    assert user.permissions == permissions
