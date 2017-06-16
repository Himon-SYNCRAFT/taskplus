import pytest
from unittest import mock

from taskplus.core.authorization import AuthorizationManager, Permission, Condition
from taskplus.core.shared.exceptions import NotAuthorized


def test_is_condition_met_returns_true():
    user = mock.Mock()
    request = mock.Mock()
    user.id = 1
    request.id = 2

    condition = Condition('user.id', 'eq', '1')
    assert condition.is_met(user, data=dict(request=request))

    condition = Condition('user.id', 'ne', '2')
    assert condition.is_met(user, data=dict(request=request))

    condition = Condition('user.id', 'ne', 'request.id')
    assert condition.is_met(user, data=dict(request=request))


def test_is_condition_met_returns_false():
    user = mock.Mock()
    request = mock.Mock()
    user.id = 2
    request.id = 2

    condition = Condition('user.id', 'eq', '1')
    assert not condition.is_met(user, data=dict(request=request))

    condition = Condition('user.id', 'ne', '2')
    assert not condition.is_met(user, data=dict(request=request))

    condition = Condition('user.id', 'ne', 'request.id')
    assert not condition.is_met(user, data=dict(request=request))


def test_authorization_manager_raise_not_authorized_without_permissions():
    user = mock.Mock()
    user.permissions = []
    action = 'ListUsersAction'
    request = mock.Mock()
    authorization_manager = AuthorizationManager()

    with pytest.raises(NotAuthorized):
        authorization_manager.authorize(user=user, action=action,
                                        data=dict(request=request))


def test_authorization_manager_with_permission():
    user = mock.Mock()
    action = 'ListUsersAction'
    request = mock.Mock()
    user.permissions = [Permission(action)]
    authorization_manager = AuthorizationManager()
    authorization_manager.authorize(user=user, action=action,
                                    data=dict(request=request))


def test_authorization_manager_permission_with_condition():
    user = mock.Mock()
    user.id = 1
    action = 'ListUsersAction'
    request = mock.Mock()
    conditions = [Condition('user.id', 'eq', '1')]
    user.permissions = [Permission(action, conditions=conditions)]
    authorization_manager = AuthorizationManager()
    authorization_manager.authorize(user=user, action=action,
                                    data=dict(request=request))


def test_authorization_manager_permission_with_multiple_conditions():
    user = mock.Mock()
    user.id = 1
    action = 'ListUsersAction'
    request = mock.Mock()
    request.id = 2
    conditions = [Condition('user.id', 'eq', '1'),
                  Condition('request.id', 'eq', '2')]
    user.permissions = [Permission(action, conditions=conditions)]
    authorization_manager = AuthorizationManager()
    authorization_manager.authorize(user=user, action=action,
                                    data=dict(request=request))


def test_authorization_manager_unmet_condition_raise_not_authorized_exc():
    user = mock.Mock()
    user.id = 1
    action = 'ListUsersAction'
    request = mock.Mock()
    conditions = [Condition('user.id', 'eq', '2')]
    user.permissions = [Permission(action, conditions=conditions)]
    authorization_manager = AuthorizationManager()

    with pytest.raises(NotAuthorized):
        authorization_manager.authorize(user=user, action=action,
                                        data=dict(request=request))
