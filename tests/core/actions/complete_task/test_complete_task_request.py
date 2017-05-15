from taskplus.core.actions import CompleteTaskRequest


def test_complete_task_request():
    task_id = 1
    request = CompleteTaskRequest(task_id)

    assert request.task_id == task_id
    assert request.is_valid()


def test_complete_task_request_without_task_id():
    task_id = None
    request = CompleteTaskRequest(task_id)

    assert request.task_id == task_id
    assert not request.is_valid()
    assert len(request.errors) == 1
    error = request.errors[0]
    assert error.parameter == 'task_id'
    assert error.message == 'is required'


def test_complete_task_bad_request():
    task_id = 'abc'
    request = CompleteTaskRequest(task_id)

    assert request.task_id == task_id
    assert not request.is_valid()
    assert len(request.errors) == 1
    error = request.errors[0]
    assert error.parameter == 'task_id'
    assert error.message == 'expected int, got str(abc)'
