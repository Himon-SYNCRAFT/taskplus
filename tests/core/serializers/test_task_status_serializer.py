import json


from taskplus.core.serializers import TaskStatusEncoder
from taskplus.core.domain import TaskStatus


def test_task_status_serializer():
    status_dict = dict(name='new', id=1)
    status = TaskStatus(**status_dict)

    expected_json = json.dumps(status_dict)

    assert json.loads(json.dumps(status, cls=TaskStatusEncoder)) ==\
        json.loads(expected_json)
