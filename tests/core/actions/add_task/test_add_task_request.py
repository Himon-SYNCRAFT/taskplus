from taskplus.core.actions import AddTaskRequest


def test_add_task_request():
    name = 'task name'
    content = 'lorem ipsum'
    creator_id = 2

    request = AddTaskRequest(name, content, creator_id)

    assert request.is_valid()
    assert request.name == name
    assert request.content == content
    assert request.creator_id == creator_id


def test_add_task_bad_request():
    name = []
    content = []
    creator_id = 'abc'

    request = AddTaskRequest(name, content, creator_id)

    assert not request.is_valid()
    assert request.name == name
    assert request.content == content
    assert request.creator_id == creator_id
    assert len(request.errors) == 3
    print(request.errors)
    assert any([param == 'name' and message == 'expected str, got list([])'
                for param, message in request.errors])
    assert any([param == 'content' and message == 'expected str, got list([])'
                for param, message in request.errors])
    assert any([param == 'creator_id' and message == 'expected int, got str(abc)'
                for param, message in request.errors])


def test_add_task_request_without_data():
    name = None
    content = None
    creator_id = None

    request = AddTaskRequest(name, content, creator_id)

    assert not request.is_valid()
    assert request.name == name
    assert request.content == content
    assert request.creator_id == creator_id
    assert len(request.errors) == 3
    assert any([e.parameter == 'name' and e.message == 'is required'
                for e in request.errors])
    assert any([e.parameter == 'content' and e.message == 'is required'
                for e in request.errors])
    assert any([e.parameter == 'creator_id' and e.message == 'is required'
                for e in request.errors])
