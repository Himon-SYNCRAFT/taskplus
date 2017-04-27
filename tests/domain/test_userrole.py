from taskplus.domain.user_role import UserRole


role_name = 'admin'


def test_role_init():
    role = UserRole(name=role_name)
    assert role.name == role_name


def test_role_from_dict():
    role = UserRole.from_dict({'name': role_name})
    assert role.name == role_name
