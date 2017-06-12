import pytest
from unittest import mock
from collections import namedtuple
from sqlalchemy import event
from sqlalchemy.engine import Engine

from taskplus.apps.rest.database import Base, db_session, engine
from taskplus.apps.rest.repositories import UsersRepository
from taskplus.core.domain import User, UserRole
from taskplus.core.shared.domain_model import DomainModel
from taskplus.core.shared.exceptions import NoResultFound


user_ = namedtuple('user_', ['id', 'name', 'role_id', 'role_name'])
creator_ = user_(id=1, name='creator', role_id=1, role_name='creator_role')
doer_ = user_(id=2, name='doer', role_id=2, role_name='doer_role')
repository = UsersRepository()


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

        creator_role = models.UserRole(name=creator_.role_name,
                                       id=creator_.role_id)
        doer_role = models.UserRole(name=doer_.role_name,
                                    id=doer_.role_id)

        db_session.add(creator_role)
        db_session.add(doer_role)
        db_session.commit()

        creator = models.User(name=creator_.name, roles=[creator_role],
                              id=creator_.id, password='pass')
        doer = models.User(name=doer_.name, roles=[doer_role],
                           id=doer_.id, password='pass')

        db_session.add(creator)
        db_session.add(doer)
        db_session.commit()


def test_users_repository_one():
    id, name, role_id, role_name = creator_
    result = repository.one(id)

    assert result.id == id
    assert result.name == name
    assert result.roles[0].id == role_id
    assert result.roles[0].name == role_name
    assert not hasattr(result, 'password')
    assert isinstance(result, DomainModel)


def test_users_repository_one_non_existing_user():
    with pytest.raises(NoResultFound):
        repository.one(99)


def test_users_repository_list():
    creator_id, creator_name, creator_role_id, creator_role_name = creator_
    doer_id, doer_name, doer_role_id, doer_role_name = doer_

    result = repository.list()

    assert len(result) == 2
    assert any([user.id == creator_id and
                user.name == creator_name and
                user.roles[0].id == creator_role_id and
                user.roles[0].name == creator_role_name
                for user in result])
    assert any([user.id == doer_id and
                user.name == doer_name and
                user.roles[0].id == doer_role_id and
                user.roles[0].name == doer_role_name
                for user in result])
    assert all([isinstance(user, DomainModel) for user in result])
    assert all([not hasattr(user, 'password') for user in result])


def test_users_repository_save():
    creator_id, creator_name, creator_role_id, creator_role_name = creator_

    user = User(
        name='user',
        roles=[UserRole(name=creator_role_name, id=creator_role_id)]
    )
    result = repository.save(user, password='pass')

    assert result.name == user.name
    assert result.roles[0].id == user.roles[0].id
    assert result.roles[0].name == user.roles[0].name
    assert not hasattr(result, 'password')
    assert isinstance(result, DomainModel)


def test_users_repository_update():
    creator_id, creator_name, creator_role_id, creator_role_name = creator_

    user = User(
        name='user',
        roles=[UserRole(name=creator_role_name, id=creator_role_id)],
        id=1
    )
    result = repository.update(user)

    assert result.id == user.id
    assert result.name == user.name
    assert result.roles[0].id == user.roles[0].id
    assert result.roles[0].name == user.roles[0].name
    assert not hasattr(result, 'password')
    assert isinstance(result, DomainModel)


def test_users_repository_with_filter_gt():
    filters = {
        'id__gt': 1
    }

    result = repository.list(filters)

    for i, user in enumerate(result):
        assert isinstance(user, DomainModel)
        assert user.id != 1

    assert len(result) == 1


def test_users_repository_with_filter_lt():
    filters = {
        'id__lt': 2
    }

    result = repository.list(filters)

    for i, user in enumerate(result):
        assert isinstance(user, DomainModel)
        assert user.id != 2

    assert len(result) == 1


def test_users_repository_with_filter_ne():
    filters = {
        'id__ne': 2
    }

    result = repository.list(filters)

    for i, user in enumerate(result):
        assert isinstance(user, DomainModel)
        assert user.id != 2

    assert len(result) == 1


def test_users_repository_with_filter_ge():
    filters = {
        'id__ge': 2
    }

    result = repository.list(filters)

    for i, user in enumerate(result):
        assert isinstance(user, DomainModel)
        assert user.id != 1

    assert any([user.id == 2 for user in result])
    assert len(result) == 1


def test_users_repository_with_filter_le():
    filters = {
        'id__le': 1
    }

    result = repository.list(filters)

    for i, user in enumerate(result):
        assert isinstance(user, DomainModel)

    assert any([user.id == 1 for user in result])
    assert len(result) == 1


def test_users_repository_delete():
    user_id = 1

    result = repository.delete(user_id)
    assert result.id == user_id
    assert not hasattr(result, 'password')

    result = repository.list()
    assert len(result) == 1
    assert all([user.id != user_id for user in result])
