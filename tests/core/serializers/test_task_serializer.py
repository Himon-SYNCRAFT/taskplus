import json

from taskplus.core.serializers import TaskEncoder
from taskplus.core.domain import User, UserRole, Task, TaskStatus


def test_user_serializer():
    task_content = 'test content'
    task_name = 'test name'

    task_dict = dict(
        name=task_name,
        content=task_content,
        status=dict(id=1, name='new'),
        creator=dict(id=1, name='creator', roles=[dict(id=1, name='creator')]),
        doer=None,
        id=1
    )

    status = TaskStatus(**(task_dict['status']))

    creator = User(
        id=task_dict['creator']['id'],
        name=task_dict['creator']['name'],
        roles=[UserRole(name=role['name'], id=role['id'])
               for role in task_dict['creator']['roles']]
    )

    task = Task(
        id=task_dict['id'],
        name=task_dict['name'],
        content=task_dict['content'],
        status=status,
        creator=creator,
        doer=None,
    )

    expected_json = json.dumps(task_dict)

    assert json.loads(json.dumps(task, cls=TaskEncoder)) ==\
        json.loads(expected_json)
