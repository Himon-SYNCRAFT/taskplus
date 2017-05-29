import pytest
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound

from taskplus.apps.rest.database import Base, db_session, engine
from taskplus.apps.rest.repositories import UserRolesRepository
from taskplus.core.domain import UserRole
from taskplus.core.shared.domain_model import DomainModel


repository = UserRolesRepository()


def setup_function():
    if db_session.bind.driver == 'pysqlite':
        @event.listens_for(Engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    from taskplus.apps.rest import models
    Base.metadata.reflect(engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    creator_role = models.UserRole(name='creator_role')
    doer_role = models.UserRole(name='doer_role')

    db_session.add(creator_role)
    db_session.add(doer_role)
    db_session.commit()


def test_user_roles_repository_list():
    result = repository.list()

    assert len(result) == 2
    assert any([role.name == 'creator_role' for role in result])
    assert any([role.name == 'doer_role' for role in result])
    assert all([isinstance(role, DomainModel) for role in result])


def test_user_roles_repository_one():
    role_id = 1
    result = repository.one(role_id)

    assert result.id == role_id
    assert isinstance(result, DomainModel)


def test_user_roles_repository_one_not_existing_role():
    role_id = 99
    with pytest.raises(NoResultFound):
        repository.one(role_id)


def test_user_roles_repository_update():
    role_id = 1
    role_name = 'test'
    role_before_update = repository.one(role_id)
    role = UserRole(id=role_id, name=role_name)
    result = repository.update(role)

    assert result.id == role_id
    assert result.name == role_name
    assert result.name != role_before_update.name
    assert isinstance(result, DomainModel)

    result = repository.list()

    assert len(result) == 2


def test_user_roles_repository_save():
    role_name = 'test'
    role = UserRole(name=role_name)

    result = repository.save(role)

    assert result.id == 3
    assert result.name == role_name
    assert isinstance(result, DomainModel)

    result = repository.list()

    assert len(result) == 3


def test_roles_repository_with_filter_gt():
    filters = {
        'id__gt': 1
    }

    result = repository.list(filters)

    for i, role in enumerate(result):
        assert isinstance(role, DomainModel)
        assert role.id != 1

    assert len(result) == 1


def test_roles_repository_with_filter_lt():
    filters = {
        'id__lt': 2
    }

    result = repository.list(filters)

    for i, role in enumerate(result):
        assert isinstance(role, DomainModel)
        assert role.id != 2

    assert len(result) == 1


def test_roles_repository_with_filter_ne():
    filters = {
        'id__ne': 2
    }

    result = repository.list(filters)

    for i, role in enumerate(result):
        assert isinstance(role, DomainModel)
        assert role.id != 2

    assert len(result) == 1


def test_roles_repository_with_filter_ge():
    filters = {
        'id__ge': 2
    }

    result = repository.list(filters)

    for i, role in enumerate(result):
        assert isinstance(role, DomainModel)
        assert role.id != 1

    assert any([role.id == 2 for role in result])
    assert len(result) == 1


def test_roles_repository_with_filter_le():
    filters = {
        'id__le': 1
    }

    result = repository.list(filters)

    for i, role in enumerate(result):
        assert isinstance(role, DomainModel)

    assert any([role.id == 1 for role in result])
    assert len(result) == 1


def test_roles_repository_delete():
    role_id = 1

    result = repository.delete(1)
    assert result.id == role_id
    assert isinstance(result, DomainModel)

    result = repository.list()
    assert all([role.id != role_id for role in result])
    assert len(result) == 1
