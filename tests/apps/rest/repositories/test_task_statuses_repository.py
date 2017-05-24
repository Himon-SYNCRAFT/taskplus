import pytest
from unittest import mock

from taskplus.apps.rest.repositories import TaskStatusesRepository
from taskplus.core.domain import TaskStatus
from taskplus.core.shared.domain_model import DomainModel


@pytest.fixture
def status():
    status = mock.Mock()
    status.id = 1
    status.name = 'new'
    return status


@pytest.fixture
def statuses():
    status_new = mock.Mock()
    status_new.id = 1
    status_new.name = 'new'

    status_done = mock.Mock()
    status_done.id = 2
    status_done.name = 'done'

    return [status_new, status_done]


def test_statuses_repository_one(status):
    repository = TaskStatusesRepository()
    repository.status_model = mock.Mock()
    repository.status_model.query.get.return_value = status
    result = repository.one(1)

    assert isinstance(result, DomainModel)
    assert result.id == status.id
    assert result.name == status.name


def test_statuses_repository_one_non_existing_status(status):
    repository = TaskStatusesRepository()
    repository.status_model = mock.Mock()
    repository.status_model.query.get.return_value = None
    result = repository.one(1)

    assert result is None


def test_statuses_repository_list(statuses):
    repository = TaskStatusesRepository()
    repository.status_model = mock.Mock()
    repository.status_model.query.all.return_value = statuses
    result = repository.list()

    for i, status in enumerate(result):
        assert isinstance(status, DomainModel)
        assert status.id == statuses[i].id
        assert status.name == statuses[i].name


def test_statuses_repository_list_with_filters(status):
    filters = {
        'name': 'new'
    }

    repository = TaskStatusesRepository()
    repository.status_model = mock.Mock()
    repository.status_model.query.all.return_value = [status]
    repository.status_model.query.filter().all.return_value = [status]
    result = repository.list(filters)[0]

    repository.status_model.query.filter.assert_called()
    assert isinstance(result, DomainModel)
    assert result.id == status.id
    assert result.name == status.name


def test_statuses_repository_update():
    repository = TaskStatusesRepository()
    repository.status_model = mock.Mock()
    repository.session = mock.Mock()
    result = repository.update(TaskStatus(id=1, name='canceled'))

    repository.session.add.assert_called_once()
    repository.session.commit.assert_called_once()
    assert isinstance(result, DomainModel)


def test_statuses_repository_save():
    repository = TaskStatusesRepository()
    repository.status_model = mock.Mock()
    repository.session = mock.Mock()
    result = repository.save(TaskStatus(name='canceled'))

    repository.session.add.assert_called_once()
    repository.session.commit.assert_called_once()
    assert isinstance(result, DomainModel)


def test_statuses_repository_work_on_real_db(status):
    repository = TaskStatusesRepository()

    filters = {
        'name': 'new'
    }

    result = repository.list(filters)[0]
    assert isinstance(result, DomainModel)

    filters = {
        'id__lt': 2
    }

    result = repository.list(filters)
    assert isinstance(result[0], DomainModel)

    result = repository.one(1)
    assert isinstance(result, DomainModel)
