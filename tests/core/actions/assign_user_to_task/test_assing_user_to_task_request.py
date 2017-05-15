from taskplus.core.actions import AssignUserToTaskRequest


def test_assign_user_to_task_request():
    user_id = 1
    task_id = 2
    request = AssignUserToTaskRequest(task_id, user_id)

    assert request.is_valid()
    assert request.task_id == task_id
    assert request.user_id == user_id


def test_assign_user_to_task_bad_request():
    user_id = 'ab'
    task_id = 'ad'

    request = AssignUserToTaskRequest(task_id, user_id)

    assert not request.is_valid()
    assert request.task_id == task_id
    assert request.user_id == user_id
    assert len(request.errors) == 2
    assert any(
        [e.parameter == 'task_id' and e.message == 'expected int, got str(ad)'
            for e in request.errors]
    )
    assert any(
        [e.parameter == 'user_id' and e.message == 'expected int, got str(ab)'
            for e in request.errors]
    )


def test_assign_user_to_task_request_without_id():
    user_id = None
    task_id = None

    request = AssignUserToTaskRequest(task_id, user_id)

    assert not request.is_valid()
    assert request.task_id == task_id
    assert request.user_id == user_id
    assert len(request.errors) == 2
    assert any([e.parameter == 'task_id' and e.message == 'is required'
                for e in request.errors])
    assert any([e.parameter == 'user_id' and e.message == 'is required'
                for e in request.errors])
