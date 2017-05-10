from taskplus.core.domain.user import User
from taskplus.core.domain.user_role import UserRole


def test_user():
    name = 'name'
    role = UserRole(name='role_name')
    user = User(name, role)

    assert user.name == name
    assert user.role == role
