import pytest
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound

from taskplus.apps.rest.database import Base, db_session, engine
from taskplus.apps.rest.repositories import TaskStatusesRepository
from taskplus.core.domain import Statuses
from taskplus.core.domain import TaskStatus
from taskplus.core.shared.domain_model import DomainModel


repository = TaskStatusesRepository()


def setup_function():
    if db_session.bind.driver == 'pysqlite':
        @event.listens_for(Engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    from taskplus.apps.rest import models
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    status_new = models.TaskStatus(id=Statuses.NEW.value, name='new')
    status_in_progress = models.TaskStatus(id=Statuses.IN_PROGRESS.value,
                                           name='in progress')
    status_completed = models.TaskStatus(id=Statuses.COMPLETED.value,
                                         name='completed')
    status_canceled = models.TaskStatus(id=Statuses.CANCELED.value, name='canceled')

    db_session.add(status_new)
    db_session.add(status_in_progress)
    db_session.add(status_canceled)
    db_session.add(status_completed)
    db_session.commit()


def test_statuses_repository_one():
    id = Statuses.NEW.value
    result = repository.one(id)

    assert isinstance(result, DomainModel)
    assert result.id == id
    assert result.name == 'new'


def test_statuses_repository_one_non_existing_status():
    with pytest.raises(NoResultFound):
        repository.one(99)


def test_statuses_repository_list():
    result = repository.list()

    for i, status in enumerate(result):
        assert isinstance(status, DomainModel)

    assert len(result) == 4


def test_statuses_repository_list_with_filters():
    filters = {
        'name': 'new'
    }

    result = repository.list(filters)[0]

    assert isinstance(result, DomainModel)
    assert result.name == 'new'


def test_statuses_repository_with_filter_gt():
    filters = {
        'id__gt': 1
    }

    result = repository.list(filters)

    for i, status in enumerate(result):
        assert isinstance(status, DomainModel)
        assert status.id != 1

    assert len(result) == 3


def test_statuses_repository_with_filter_lt():
    filters = {
        'id__lt': 4
    }

    result = repository.list(filters)

    for i, status in enumerate(result):
        assert isinstance(status, DomainModel)
        assert status.id != 4

    assert len(result) == 3


def test_statuses_repository_with_filter_ne():
    filters = {
        'id__ne': 2
    }

    result = repository.list(filters)

    for i, status in enumerate(result):
        assert isinstance(status, DomainModel)
        assert status.id != 2

    assert len(result) == 3


def test_statuses_repository_with_filter_ge():
    filters = {
        'id__ge': 2
    }

    result = repository.list(filters)

    for i, status in enumerate(result):
        assert isinstance(status, DomainModel)
        assert status.id != 1

    assert any([status.id == 2 for status in result])
    assert len(result) == 3


def test_statuses_repository_with_filter_le():
    filters = {
        'id__le': 2
    }

    result = repository.list(filters)

    for i, status in enumerate(result):
        assert isinstance(status, DomainModel)

    assert any([status.id == 1 for status in result])
    assert any([status.id == 2 for status in result])
    assert len(result) == 2


def test_statuses_repository_update():
    id = 1
    name = 'suspended'

    result = repository.update(TaskStatus(id=id, name=name))

    assert isinstance(result, DomainModel)
    assert result.id == id
    assert result.name == name


def test_statuses_repository_save():
    status_name = 'suspended'
    result = repository.save(TaskStatus(name=status_name))

    assert isinstance(result, DomainModel)
    assert result.name == status_name


def test_statuses_repository_delete():
    id = Statuses.NEW.value
    result = repository.delete(id)
    statuses = repository.list()

    assert isinstance(result, DomainModel)
    assert result.id == id
    assert len(statuses) == 3
    assert all([status.id != id and status.name != 'new' for status in statuses])
