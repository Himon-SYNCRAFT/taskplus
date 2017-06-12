import json

from taskplus.core.serializers import UserEncoder
from taskplus.core.domain import User, UserRole


def test_user_serializer():
    role = UserRole(name='admin', id=1)
    role2 = UserRole(name='creator', id=2)
    user = User(name='user', roles=[role, role2])

    expected_json = json.dumps(dict(
        id=None,
        name=user.name,
        roles=[
            dict(name=role.name, id=role.id),
            dict(name=role2.name, id=role2.id)
        ],
    ))

    assert json.loads(json.dumps(user, cls=UserEncoder)) ==\
        json.loads(expected_json)
