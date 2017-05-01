import pytest

from taskplus.core.shared.domain_model import DomainModel
from taskplus.core.repository.memory.user_roles_memrepo import UserRolesRepo


role1 = dict(name='admin')
role2 = dict(name='doer')
role3 = dict(name='creator')


@pytest.fixture
def roles():
    return [role1, role2, role3]


def _check_results(domain_model_list, data_list):
    assert len(domain_model_list) == len(data_list)
    assert all([isinstance(dm, DomainModel) for dm in domain_model_list])
    assert set([dm.name for dm in domain_model_list]) ==\
        set([d['name'] for d in data_list])


def test_repository_list_without_parameters(roles):
    repo = UserRolesRepo(roles)
    assert repo.list() == roles


def test_repository_list_with_filters_unknown_key(roles):
    repo = UserRolesRepo(roles)

    with pytest.raises(KeyError):
        repo.list(filters={'some_key': 'some_value'})


def test_repository_list_with_filters_unknown_operator(roles):
    repo = UserRolesRepo(roles)

    with pytest.raises(ValueError):
        repo.list(filters={'name__gt': 'admin'})


def test_repository_list_with_filters_name(roles):
    repo = UserRolesRepo(roles)

    _check_results(repo.list(filters={'name': 'creator'}), [role3])
