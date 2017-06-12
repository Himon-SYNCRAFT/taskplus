from taskplus.core.domain import Task, User, TaskStatus, UserRole
from taskplus.core.shared.domain_model import DomainModel


def test_task():
    role_creator = UserRole(name='creator')
    role_doer = UserRole(name='doer')
    task_name = 'example name'
    task_content = 'lorem ipsum'
    task_status = TaskStatus(name='new', id=1)
    task_creator = User(name='creator', roles=[role_creator])
    task_doer = User(name='doer', roles=[role_doer])
    task_id = 1

    task = Task(name=task_name, content=task_content, status=task_status,
                creator=task_creator, doer=task_doer, id=task_id)

    assert task.name == task_name
    assert task.content == task_content
    assert task.status == task_status
    assert task.creator == task_creator
    assert task.doer == task_doer
    assert task.id == task_id
    assert isinstance(task, DomainModel)
