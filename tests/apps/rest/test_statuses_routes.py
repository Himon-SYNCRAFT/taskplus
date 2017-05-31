
import json
from unittest import mock

from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.domain import TaskStatus


status = TaskStatus(name='new', id=1)
statuses = [status]


@mock.patch('taskplus.apps.rest.routes.ListTaskStatusesAction')
def test_get_statuses_list(mock_action, client):
    response = ResponseSuccess(statuses)
    mock_action().execute.return_value = response

    http_response = client.get('/statuses')

    assert json.loads(http_response.data.decode('UTF-8')) == [{
        'name': status.name,
        'id': status.id
    }]
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.ListTaskStatusesAction')
def test_get_statuses_list_with_filters(mock_action, client):
    response = ResponseSuccess(statuses)
    mock_action().execute.return_value = response

    data = json.dumps(dict(filters=dict(name='new')))
    http_response = client.post('/statuses', data=data,
                                content_type='application/json')

    assert json.loads(http_response.data.decode('UTF-8')) == [{
        'name': status.name,
        'id': status.id
    }]
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.GetTaskStatusDetailsAction')
def test_get_status_details(mock_action, client):
    response = ResponseSuccess(status)
    mock_action().execute.return_value = response

    http_response = client.get('/status/{}'.format(status.id))

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': status.name,
        'id': status.id
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.AddTaskStatusAction')
def test_add_status(mock_action, client):
    response = ResponseSuccess(status)
    mock_action().execute.return_value = response

    data = json.dumps(dict(name=status.name))
    http_response = client.post('/status', data=data,
                                content_type='application/json')

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': status.name,
        'id': status.id
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.DeleteTaskStatusAction')
def test_delete_status(mock_action, client):
    response = ResponseSuccess(status)
    mock_action().execute.return_value = response

    http_response = client.delete('/status/{}'.format(status.id))

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': status.name,
        'id': status.id
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.UpdateTaskStatusAction')
def test_update_status(mock_action, client):
    response = ResponseSuccess(status)
    mock_action().execute.return_value = response
    data = json.dumps(dict(id=status.id, name=status.name))

    http_response = client.put('/status', data=data,
                               content_type='application/json')

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': status.name,
        'id': status.id
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'
