from taskplus.core.domain.user_role import UserRole


role_name = 'admin'


def test_role_init():
    role = UserRole(name=role_name)
    assert role.name == role_name
