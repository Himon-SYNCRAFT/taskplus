import pytest
from unittest import mock

from taskplus.core.authorization import AuthorizationManager, Permission, Condition
from taskplus.core.shared.exceptions import NotAuthorized
from taskplus.core.actions import ListUsersAction


def test_authorization_manager_raise_not_authorized_without_permissions():
    user = mock.Mock()
    user.permissions = []
    action = mock.Mock()
    request = mock.Mock()
    authorization_manager = AuthorizationManager()

    with pytest.raises(NotAuthorized):
        authorization_manager.authorize(user, action, request)


def test_authorization_manager_with_permission():
    user = mock.Mock()
    action = ListUsersAction(mock.Mock())
    request = mock.Mock()
    user.permissions = [Permission(action.get_name())]
    authorization_manager = AuthorizationManager()
    authorization_manager.authorize(user, action, request)


def test_authorization_manager_permission_with_condition():
    user = mock.Mock()
    user.id = '1'
    action = ListUsersAction(mock.Mock())
    request = mock.Mock()
    conditions = [Condition('user.id', 'eq', '1')]
    user.permissions = [Permission(action.get_name(), conditions=conditions)]
    authorization_manager = AuthorizationManager()
    authorization_manager.authorize(user, action, request)


def test_authorization_manager_permission_with_multiple_conditions():
    user = mock.Mock()
    user.id = '1'
    action = ListUsersAction(mock.Mock())
    request = mock.Mock()
    request.id = '2'
    conditions = [Condition('user.id', 'eq', '1'),
                  Condition('request.id', 'eq', '2')]
    user.permissions = [Permission(action.get_name(), conditions=conditions)]
    authorization_manager = AuthorizationManager()
    authorization_manager.authorize(user, action, request)


def test_authorization_manager_unmet_condition_raise_not_authorized_exc():
    user = mock.Mock()
    user.id = '1'
    action = ListUsersAction(mock.Mock())
    request = mock.Mock()
    conditions = [Condition('user.id', 'eq', '2')]
    user.permissions = [Permission(action.get_name(), conditions=conditions)]
    authorization_manager = AuthorizationManager()

    with pytest.raises(NotAuthorized):
        authorization_manager.authorize(user, action, request)
