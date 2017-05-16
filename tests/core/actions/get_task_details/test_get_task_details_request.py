from taskplus.core.actions import GetTaskDetailsRequest


def test_get_task_details_request():
    task_id = 1
    request = GetTaskDetailsRequest(task_id)

    assert request.is_valid()
    assert request.task_id == task_id


def test_get_task_details_request_without_id():
    task_id = None
    request = GetTaskDetailsRequest(task_id)

    assert not request.is_valid()
    assert request.task_id == task_id
    assert len(request.errors) == 1
    error = request.errors[0]
    assert error.parameter == 'task_id'
    assert error.message == 'is required'


def test_get_task_details_bad_request():
    task_id = 'asd'
    request = GetTaskDetailsRequest(task_id)

    assert not request.is_valid()
    assert request.task_id == task_id
    assert len(request.errors) == 1
    error = request.errors[0]
    assert error.parameter == 'task_id'
    assert error.message == 'expected int, got str(asd)'
