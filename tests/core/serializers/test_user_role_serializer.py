import json

from taskplus.core.serializers.user_role_serializer import UserRoleEncoder
from taskplus.core.domain.user_role import UserRole


def test_serialize_role():
    role = UserRole(name='admin')
    expected_json = json.dumps({'name': 'admin'})
    assert json.loads(json.dumps(role, cls=UserRoleEncoder)) ==\
        json.loads(expected_json)
