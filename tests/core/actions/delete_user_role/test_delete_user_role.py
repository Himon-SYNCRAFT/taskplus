from unittest import mock

from taskplus.core.actions import DeleteUserRoleAction
from taskplus.core.actions import DeleteUserRoleRequest


def test_delete_user_role():
    user_role_id = 1
    request = DeleteUserRoleRequest(id=user_role_id)
    repo = mock.Mock()
    repo.delete.return_value = user_role_id

    action = DeleteUserRoleAction(repo=repo)
    response = action.execute(request)

    assert repo.delete.called
    assert bool(response) is True
    assert response.value == repo.delete.return_value


def test_delete_user_role_with_hooks():
    user_role_id = 1
    request = DeleteUserRoleRequest(id=user_role_id)
    repo = mock.Mock()
    repo.delete.return_value = user_role_id

    action = DeleteUserRoleAction(repo=repo)

    before = mock.MagicMock()
    after = mock.MagicMock()

    action.add_before_execution_hook(before)
    action.add_after_execution_hook(after)

    response = action.execute(request)

    assert before.called
    assert after.called

    assert repo.delete.called
    assert bool(response) is True
    assert response.value == repo.delete.return_value
