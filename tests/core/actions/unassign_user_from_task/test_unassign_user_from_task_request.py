from taskplus.core.actions import UnassignUserFromTaskRequest


def test_unassign_user_from_task_request():
    task_id = 1
    request = UnassignUserFromTaskRequest(task_id)

    assert request.is_valid()
    assert request.task_id == task_id


def test_unassign_user_from_task_request_without_id():
    task_id = None
    request = UnassignUserFromTaskRequest(task_id)

    assert not request.is_valid()
    assert request.task_id == task_id
    assert len(request.errors) == 1
    error = request.errors[0]
    assert error.parameter == 'task_id'
    assert error.message == 'is required'


def test_unassign_user_from_task_bad_reqes():
    task_id = 'abc'
    request = UnassignUserFromTaskRequest(task_id)

    assert not request.is_valid()
    assert request.task_id == task_id
    assert len(request.errors) == 1
    error = request.errors[0]
    assert error.parameter == 'task_id'
    assert error.message == 'expected int, got str(abc)'
