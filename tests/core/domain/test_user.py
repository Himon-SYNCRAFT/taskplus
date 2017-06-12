from taskplus.core.domain import User, UserRole


def test_user():
    name = 'name'
    roles = [UserRole(name='role_name'), UserRole(name="role_name2")]
    user = User(name=name, roles=roles)

    assert user.name == name
    assert user.roles == roles
