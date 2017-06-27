import pytest
from unittest import mock
from sqlalchemy import event
from sqlalchemy.engine import Engine

from taskplus.apps.rest.database import Base, db_session, engine
from taskplus.apps.rest.repositories import TasksRepository
from taskplus.core.domain import Statuses, Task, User, TaskStatus, UserRole
from taskplus.core.shared.domain_model import DomainModel
from taskplus.core.shared.exceptions import NoResultFound


repository = TasksRepository()


def setup_function(function):
    if db_session.bind.driver == 'pysqlite':
        @event.listens_for(Engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    with mock.patch('taskplus.apps.rest.models.User._hash_password',
                    side_effect=lambda x: x):
        from taskplus.apps.rest import models
        Base.metadata.reflect(engine)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        creator_role = models.UserRole(name='creator_role')
        doer_role = models.UserRole(name='doer_role')

        db_session.add(creator_role)
        db_session.add(doer_role)
        db_session.commit()

        creator = models.User(name='creator', roles=[creator_role],
                              password='pass')
        doer = models.User(name='doer', roles=[doer_role], password='pass')

        db_session.add(creator)
        db_session.add(doer)
        db_session.commit()

        status_new = models.TaskStatus(id=Statuses.NEW, name='new')
        status_in_progress = models.TaskStatus(
            id=Statuses.IN_PROGRESS, name='in progress')

        db_session.add(status_new)
        db_session.add(status_in_progress)
        db_session.commit()

        task = models.Task(name='example task 1', content='lorem ipsum',
                           status_id=status_new.id, creator_id=creator.id,
                           doer_id=doer.id)
        task2 = models.Task(name='example task 2', content='lorem ipsum 2',
                            status_id=status_new.id, creator_id=creator.id,
                            doer_id=doer.id)

        db_session.add(task)
        db_session.add(task2)
        db_session.commit()


def test_tasks_repository_one():
    task_id = 1
    task = repository.one(task_id)

    assert task.id == task_id
    assert task.content == 'lorem ipsum'
    assert task.creator.name == 'creator'
    assert task.creator.roles[0].name == 'creator_role'
    assert task.doer.name == 'doer'
    assert task.doer.roles[0].name == 'doer_role'
    assert task.status.name == 'new'
    assert isinstance(task, DomainModel)


def test_tasks_repository_not_existing_task():
    with pytest.raises(NoResultFound):
        repository.one(99)


def test_tasks_repository_list():
    result = repository.list()

    assert len(result) == 2
    assert all([isinstance(task, DomainModel) for task in result])


def test_tasks_repository_with_filter_gt():
    filters = {
        'id__gt': 1
    }

    result = repository.list(filters)

    for i, task in enumerate(result):
        assert isinstance(task, DomainModel)
        assert task.id != 1

    assert len(result) == 1


def test_tasks_repository_with_filter_lt():
    filters = {
        'id__lt': 2
    }

    result = repository.list(filters)

    for i, task in enumerate(result):
        assert isinstance(task, DomainModel)
        assert task.id != 2

    assert len(result) == 1


def test_tasks_repository_with_filter_ne():
    filters = {
        'id__ne': 2
    }

    result = repository.list(filters)

    for i, task in enumerate(result):
        assert isinstance(task, DomainModel)
        assert task.id != 2

    assert len(result) == 1


def test_tasks_repository_with_filter_ge():
    filters = {
        'id__ge': 2
    }

    result = repository.list(filters)

    for i, task in enumerate(result):
        assert isinstance(task, DomainModel)
        assert task.id != 1

    assert any([task.id == 2 for task in result])
    assert len(result) == 1


def test_tasks_repository_with_filter_in():
    filters = {
        'id__in': [1, 2]
    }

    result = repository.list(filters)

    for i, task in enumerate(result):
        assert isinstance(task, DomainModel)

    assert len(result) == 2


def test_tasks_repository_with_filter_notin():
    filters = {
        'id__notin': [2]
    }

    result = repository.list(filters)

    for i, task in enumerate(result):
        assert isinstance(task, DomainModel)
        assert task.id != 2

    assert len(result) == 1


def test_tasks_repository_with_filter_le():
    filters = {
        'id__le': 1
    }

    result = repository.list(filters)

    for i, task in enumerate(result):
        assert isinstance(task, DomainModel)

    assert any([task.id == 1 for task in result])
    assert len(result) == 1


def test_tasks_repository_filter_by_status_name():
    filters = {
        'status_name': 'new'
    }

    result = repository.list(filters)

    assert all([isinstance(task, DomainModel) for task in result])
    assert all([task.status.name == 'new' for task in result])
    assert len(result) == 2


def test_tasks_repository_filter_by_status_id():
    filters = {
        'status_id': 1
    }

    result = repository.list(filters)

    assert all([isinstance(task, DomainModel) for task in result])
    assert all([task.status.id == 1 for task in result])
    assert len(result) == 2


def test_tasks_repository_filter_by_creator_name():
    filters = {
        'creator_name': 'creator'
    }

    result = repository.list(filters)

    assert all([isinstance(task, DomainModel) for task in result])
    assert all([task.creator.name == 'creator' for task in result])
    assert len(result) == 2


def test_tasks_repository_filter_by_creator_id():
    filters = {
        'creator_id': 1
    }

    result = repository.list(filters)

    assert all([isinstance(task, DomainModel) for task in result])
    assert all([task.creator.id == 1 for task in result])
    assert len(result) == 2


def test_tasks_repository_filter_by_doer_name():
    filters = {
        'doer_name': 'doer'
    }

    result = repository.list(filters)

    assert all([isinstance(task, DomainModel) for task in result])
    assert all([task.doer.name == 'doer' for task in result])
    assert len(result) == 2


def test_tasks_repository_filter_by_doer_id():
    filters = {
        'doer_id': 2
    }

    result = repository.list(filters)

    assert all([isinstance(task, DomainModel) for task in result])
    assert all([task.doer.id == 2 for task in result])
    assert len(result) == 2


def test_tasks_repository_update():
    task_content = 'test content'
    task_status_id = 2
    task_creator_id = 2
    task_doer_id = 1

    task = repository.one(1)
    assert task.content != task_content
    assert task.status.id != task_status_id
    assert task.creator.id != task_creator_id
    assert task.doer.id != task_doer_id

    task.content = task_content
    task.status.id = task_status_id
    task.creator.id = task_creator_id
    task.doer.id = task_doer_id
    repository.update(task)
    task = repository.one(1)

    assert task.content == task_content
    assert task.status.id == task_status_id
    assert task.creator.id == task_creator_id
    assert task.doer.id == task_doer_id
    assert isinstance(task, DomainModel)
    assert len(repository.list()) == 2


def test_tasks_repository_update_not_existing_task():
    task = Task(
        name='task_name',
        content='task_content',
        status=TaskStatus(id=1, name='new'),
        creator=User(id=1, name='creator', roles=[UserRole(id=1, name='creator')]),
        doer=None,
        id=9
    )

    with pytest.raises(NoResultFound):
        repository.update(task)


def test_tasks_repository_update_with_not_existing_status():
    task_content = 'test content'
    task_name = 'test name'

    task = Task(
        name=task_name,
        content=task_content,
        status=TaskStatus(id=9, name='new'),
        creator=User(id=1, name='creator', roles=[UserRole(id=1, name='creator')]),
        doer=None,
        id=1
    )

    with pytest.raises(NoResultFound):
        repository.update(task)


def test_tasks_repository_update_with_not_existing_creator():
    task_content = 'test content'
    task_name = 'test name'

    task = Task(
        name=task_name,
        content=task_content,
        status=TaskStatus(id=1, name='new'),
        creator=User(id=9, name='creator', roles=[UserRole(id=1, name='creator')]),
        doer=None,
        id=1
    )

    with pytest.raises(NoResultFound):
        repository.update(task)


def test_tasks_repository_update_with_not_existing_doer():
    task_content = 'test content'
    task_name = 'test name'

    task = Task(
        name=task_name,
        content=task_content,
        status=TaskStatus(id=1, name='new'),
        creator=User(id=1, name='creator', roles=[UserRole(id=1, name='creator')]),
        doer=User(id=9, name='creator', roles=[UserRole(id=1, name='creator')]),
        id=1
    )

    with pytest.raises(NoResultFound):
        repository.update(task)


def test_tasks_repository_save():
    task_content = 'test content'
    task_name = 'test name'

    task = Task(
        name=task_name,
        content=task_content,
        status=TaskStatus(id=1, name='new'),
        creator=User(id=1, name='creator', roles=[UserRole(id=1, name='creator')]),
        doer=None,
    )

    result = repository.save(task)

    assert result.name == task_name
    assert result.content == task_content
    assert result.status.id == 1
    assert result.creator.id == 1
    assert result.doer is None
    assert isinstance(result, DomainModel)
    assert len(repository.list()) == 3


def test_tasks_repository_save_with_not_existing_status():
    task_content = 'test content'
    task_name = 'test name'

    task = Task(
        name=task_name,
        content=task_content,
        status=TaskStatus(id=9, name='new'),
        creator=User(id=1, name='creator', roles=[UserRole(id=1, name='creator')]),
        doer=None,
    )

    with pytest.raises(NoResultFound):
        repository.save(task)


def test_tasks_repository_save_with_not_existing_creator():
    task_content = 'test content'
    task_name = 'test name'

    task = Task(
        name=task_name,
        content=task_content,
        status=TaskStatus(id=1, name='new'),
        creator=User(id=9, name='creator', roles=[UserRole(id=1, name='creator')]),
        doer=None,
    )

    with pytest.raises(NoResultFound):
        repository.save(task)


def test_tasks_repository_save_with_not_existing_doer():
    task_content = 'test content'
    task_name = 'test name'

    task = Task(
        name=task_name,
        content=task_content,
        status=TaskStatus(id=1, name='new'),
        creator=User(id=1, name='creator', roles=[UserRole(id=1, name='creator')]),
        doer=User(id=9, name='creator', roles=[UserRole(id=1, name='creator')]),
    )

    with pytest.raises(NoResultFound):
        repository.save(task)


def test_tasks_repository_delete():
    task_id = 1
    result = repository.delete(task_id)
    assert result.id == task_id
    assert isinstance(result, DomainModel)

    result = repository.list()
    assert len(result) == 1
    assert all([task.id != task_id for task in result])


def test_tasks_repository_delete_not_existng_task():
    with pytest.raises(NoResultFound):
        repository.delete(9)
