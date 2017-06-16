from unittest import mock

from taskplus.core.actions import DeleteTaskStatusAction, DeleteTaskStatusRequest


def test_delete_task_status_request():
    task_status_id = 1
    request = DeleteTaskStatusRequest(id=task_status_id)

    assert request.is_valid() is True
    assert request.id == task_status_id


def test_delete_task_status_request_without_id():
    request = DeleteTaskStatusRequest(id=None)

    assert request.is_valid() is False
    assert request.id is None


def test_delete_task_status():
    task_status_id = 1
    request = DeleteTaskStatusRequest(id=task_status_id)
    repo = mock.Mock()
    repo.delete.return_value = task_status_id

    action = DeleteTaskStatusAction(repo=repo)
    response = action.execute(request)

    assert repo.delete.called
    assert bool(response) is True
    assert response.value == repo.delete.return_value


def test_delete_task_status_with_hooks():
    task_status_id = 1
    request = DeleteTaskStatusRequest(id=task_status_id)
    repo = mock.Mock()
    repo.delete.return_value = task_status_id

    action = DeleteTaskStatusAction(repo=repo)

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
