from collections import namedtuple
from sqlalchemy import event
from sqlalchemy.engine import Engine

from taskplus.apps.rest.database import Base, db_session, engine
from taskplus.apps.rest.repositories import UsersRepository
from taskplus.core.domain import User, UserRole
from taskplus.core.shared.domain_model import DomainModel


user_ = namedtuple('user_', ['id', 'name', 'role_id', 'role_name'])
creator_ = user_(id=1, name='creator', role_id=1, role_name='creator_role')
doer_ = user_(id=2, name='doer', role_id=2, role_name='doer_role')


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

    creator_role = models.UserRole(name=creator_.role_name,
                                   id=creator_.role_id)
    doer_role = models.UserRole(name=doer_.role_name,
                                id=doer_.role_id)

    db_session.add(creator_role)
    db_session.add(doer_role)
    db_session.commit()

    creator = models.User(name=creator_.name, role_id=creator_role.id,
                          id=creator_.id)
    doer = models.User(name=doer_.name, role_id=doer_role.id,
                       id=doer_.id)

    db_session.add(creator)
    db_session.add(doer)
    db_session.commit()


def test_users_repository_one():
    id, name, role_id, role_name = creator_
    repo = UsersRepository()
    result = repo.one(id)

    assert result.id == id
    assert result.name == name
    assert result.role.id == role_id
    assert result.role.name == role_name
    assert isinstance(result, DomainModel)


def test_users_repository_one_non_existing_user():
    repo = UsersRepository()
    result = repo.one(99)

    assert result is None


def test_users_repository_list():
    creator_id, creator_name, creator_role_id, creator_role_name = creator_
    doer_id, doer_name, doer_role_id, doer_role_name = doer_

    repo = UsersRepository()
    result = repo.list()

    assert len(result) == 2
    assert any([user.id == creator_id and
                user.name == creator_name and
                user.role.id == creator_role_id and
                user.role.name == creator_role_name
                for user in result])
    assert any([user.id == doer_id and
                user.name == doer_name and
                user.role.id == doer_role_id and
                user.role.name == doer_role_name
                for user in result])
    assert all([isinstance(user, DomainModel) for user in result])


def test_users_repository_save():
    creator_id, creator_name, creator_role_id, creator_role_name = creator_

    user = User(
        name='user',
        role=UserRole(name=creator_role_name, id=creator_role_id)
    )
    repo = UsersRepository()
    result = repo.save(user)

    assert result.name == user.name
    assert result.role.id == user.role.id
    assert result.role.name == user.role.name
    assert isinstance(result, DomainModel)


def test_users_repository_update():
    creator_id, creator_name, creator_role_id, creator_role_name = creator_

    user = User(
        name='user',
        role=UserRole(name=creator_role_name, id=creator_role_id),
        id=1
    )
    repo = UsersRepository()
    result = repo.update(user)

    assert result.id == user.id
    assert result.name == user.name
    assert result.role.id == user.role.id
    assert result.role.name == user.role.name
    assert isinstance(result, DomainModel)
