import json

from taskplus.core.serializers import UserEncoder
from taskplus.core.domain import User, UserRole


def test_user_serializer():
    role = UserRole(name='admin', id=1)
    user = User(name='user', role=role)

    expected_json = json.dumps(dict(
        name=user.name, role=dict(name=role.name, id=role.id), id=None))

    assert json.loads(json.dumps(user, cls=UserEncoder)) ==\
        json.loads(expected_json)
