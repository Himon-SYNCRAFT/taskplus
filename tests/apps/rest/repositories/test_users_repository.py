import pytest
from unittest import mock

from taskplus.apps.rest.repositories import UsersRepository
from taskplus.core.domain import User, UserRole
from taskplus.core.shared.domain_model import DomainModel


@pytest.fixture
def user():
    role = mock.Mock()
    role.id = 1
    role.name = 'creator'

    user = mock.Mock()
    user.role = role
    user.name = 'user'
    user.id = 1

    return user


@pytest.fixture
def users():
    creator_role = mock.Mock()
    creator_role.id = 1
    creator_role.name = 'creator'

    doer_role = mock.Mock()
    doer_role.id = 2
    doer_role.name = 'doer'

    creator = mock.Mock()
    creator.role = creator_role
    creator.name = 'creator1'
    creator.id = 1

    doer = mock.Mock()
    doer.role = doer_role
    doer.name = 'doer1'
    doer.id = 2

    return [creator, doer]


def test_users_repository_one(user):
    repo = UsersRepository()
    repo.user_model = mock.Mock()
    repo.user_model.query.get.return_value = user
    result = repo.one(1)

    assert result.id == user.id
    assert result.name == user.name
    assert result.role.id == user.role.id
    assert result.role.name == user.role.name
    assert isinstance(result, DomainModel)


def test_users_repository_one_non_existing_user(user):
    repo = UsersRepository()
    repo.user_model = mock.Mock()
    repo.user_model.query.get.return_value = None
    result = repo.one(1)

    assert result is None


def test_users_repository_list(users):
    repo = UsersRepository()
    repo.user_model = mock.Mock()
    repo.user_model.query.all.return_value = users
    result = repo.list()

    assert len(result) == len(users)
    for user in users:
        assert any([u.id == user.id and u.name == user.name
                    and u.role.id == user.role.id and u.role.name == user.role.name
                    for u in result])
    assert all([isinstance(user, DomainModel) for user in result])


def test_users_repository_save():
    user = User(
        name='user',
        role=UserRole(name='creator', id=1)
    )
    repo = UsersRepository()
    repo.user_model = mock.Mock()
    repo.session = mock.Mock()

    repo.save(user)

    repo.session.add.assert_called_once()
    repo.session.commit.assert_called_once()


def test_users_repository_update():
    user = User(
        name='user',
        role=UserRole(name='creator', id=1)
    )
    repo = UsersRepository()
    repo.user_model = mock.Mock()
    repo.session = mock.Mock()

    repo.update(user)

    repo.session.add.assert_called_once()
    repo.session.commit.assert_called_once()
