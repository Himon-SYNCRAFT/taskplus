import json
import pytest
from unittest import mock

from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.domain import User, UserRole, Task, TaskStatus, Statuses


doer_role = UserRole(name='doer_role', id=2)
creator_role = UserRole(name='creator_role', id=1)
creator = User(name='creator', role=creator_role, id=1)
doer = User(name='doer', role=doer_role, id=2)
status_new = TaskStatus(id=Statuses.NEW.value, name='new')


@pytest.fixture()
def task():
    task = Task(name='example task 1', content='lorem ipsum',
                status=status_new, creator=creator,
                doer=doer, id=1)

    return task


@pytest.fixture()
def tasks():
    task = Task(name='example task 1', content='lorem ipsum',
                status=status_new, creator=creator,
                doer=doer, id=1)
    tasks = [task]

    return tasks


@mock.patch('taskplus.apps.rest.routes.ListTasksAction')
def test_get_tasks_list(mock_action, client, task, tasks):
    response = ResponseSuccess(tasks)
    mock_action().execute.return_value = response

    http_response = client.get('/tasks')

    assert json.loads(http_response.data.decode('UTF-8')) == [{
        'name': task.name,
        'content': task.content,
        'id': task.id,
        'status': {
            'id': task.status.id,
            'name': task.status.name,
        },
        'doer': {
            'id': task.doer.id,
            'name': task.doer.name,
            'role': {
                'id': task.doer.role.id,
                'name': task.doer.role.name,
            }
        },
        'creator': {
            'id': task.creator.id,
            'name': task.creator.name,
            'role': {
                'id': task.creator.role.id,
                'name': task.creator.role.name,
            }
        },
    }]
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.GetNotCompletedTasksAction')
def test_get_not_completed_tasks(mock_action, client, task, tasks):
    response = ResponseSuccess(tasks)
    mock_action().execute.return_value = response

    http_response = client.get('/tasks/notcompleted')

    assert json.loads(http_response.data.decode('UTF-8')) == [{
        'name': task.name,
        'content': task.content,
        'id': task.id,
        'status': {
            'id': task.status.id,
            'name': task.status.name,
        },
        'doer': {
            'id': task.doer.id,
            'name': task.doer.name,
            'role': {
                'id': task.doer.role.id,
                'name': task.doer.role.name,
            }
        },
        'creator': {
            'id': task.creator.id,
            'name': task.creator.name,
            'role': {
                'id': task.creator.role.id,
                'name': task.creator.role.name,
            }
        },
    }]
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.ListTasksAction')
def test_get_tasks_list_with_filters(mock_action, client, task, tasks):
    response = ResponseSuccess(tasks)
    mock_action().execute.return_value = response

    data = json.dumps(dict(filters=dict(name=task.name)))
    http_response = client.post('/tasks', data=data,
                                content_type='application/json')

    assert json.loads(http_response.data.decode('UTF-8')) == [{
        'name': task.name,
        'content': task.content,
        'id': task.id,
        'status': {
            'id': task.status.id,
            'name': task.status.name,
        },
        'doer': {
            'id': task.doer.id,
            'name': task.doer.name,
            'role': {
                'id': task.doer.role.id,
                'name': task.doer.role.name,
            }
        },
        'creator': {
            'id': task.creator.id,
            'name': task.creator.name,
            'role': {
                'id': task.creator.role.id,
                'name': task.creator.role.name,
            }
        },
    }]
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.GetTaskDetailsAction')
def test_get_task_details(mock_action, client, task, tasks):
    response = ResponseSuccess(task)
    mock_action().execute.return_value = response

    http_response = client.get('/task/{}'.format(task.id))

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': task.name,
        'content': task.content,
        'id': task.id,
        'status': {
            'id': task.status.id,
            'name': task.status.name,
        },
        'doer': {
            'id': task.doer.id,
            'name': task.doer.name,
            'role': {
                'id': task.doer.role.id,
                'name': task.doer.role.name,
            }
        },
        'creator': {
            'id': task.creator.id,
            'name': task.creator.name,
            'role': {
                'id': task.creator.role.id,
                'name': task.creator.role.name,
            }
        },
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.AddTaskAction')
def test_add_task(mock_action, client, task, tasks):
    response = ResponseSuccess(task)
    mock_action().execute.return_value = response

    data = json.dumps(dict(name=task.name, content='lorem ipsum',
                           creator_id=creator.id))
    http_response = client.post('/task', data=data,
                                content_type='application/json')

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': task.name,
        'content': task.content,
        'id': task.id,
        'status': {
            'id': task.status.id,
            'name': task.status.name,
        },
        'doer': {
            'id': task.doer.id,
            'name': task.doer.name,
            'role': {
                'id': task.doer.role.id,
                'name': task.doer.role.name,
            }
        },
        'creator': {
            'id': task.creator.id,
            'name': task.creator.name,
            'role': {
                'id': task.creator.role.id,
                'name': task.creator.role.name,
            }
        },
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.CancelTaskAction')
def test_cancel_task(mock_action, client, task, tasks):
    task.status = TaskStatus(id=Statuses.CANCELED.value, name='canceled')
    response = ResponseSuccess(task)
    mock_action().execute.return_value = response

    http_response = client.get('/task/{}/cancel'.format(task.id))

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': task.name,
        'content': task.content,
        'id': task.id,
        'status': {
            'id': task.status.id,
            'name': task.status.name,
        },
        'doer': {
            'id': task.doer.id,
            'name': task.doer.name,
            'role': {
                'id': task.doer.role.id,
                'name': task.doer.role.name,
            }
        },
        'creator': {
            'id': task.creator.id,
            'name': task.creator.name,
            'role': {
                'id': task.creator.role.id,
                'name': task.creator.role.name,
            }
        },
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.CompleteTaskAction')
def test_completed_task(mock_action, client, task, tasks):
    task.status = TaskStatus(id=Statuses.COMPLETED.value, name='completed')
    response = ResponseSuccess(task)
    mock_action().execute.return_value = response

    http_response = client.get('/task/{}/complete'.format(task.id))

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': task.name,
        'content': task.content,
        'id': task.id,
        'status': {
            'id': task.status.id,
            'name': task.status.name,
        },
        'doer': {
            'id': task.doer.id,
            'name': task.doer.name,
            'role': {
                'id': task.doer.role.id,
                'name': task.doer.role.name,
            }
        },
        'creator': {
            'id': task.creator.id,
            'name': task.creator.name,
            'role': {
                'id': task.creator.role.id,
                'name': task.creator.role.name,
            }
        },
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.AssignUserToTaskAction')
def test_assign_user_to_task(mock_action, client, task, tasks):
    task.doer = User(id=3, name='test', role=doer_role)
    response = ResponseSuccess(task)
    mock_action().execute.return_value = response

    http_response = client.get('/task/{}/assign/{}'.format(task.id,
                                                           task.doer.id))

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': task.name,
        'content': task.content,
        'id': task.id,
        'status': {
            'id': task.status.id,
            'name': task.status.name,
        },
        'doer': {
            'id': task.doer.id,
            'name': task.doer.name,
            'role': {
                'id': task.doer.role.id,
                'name': task.doer.role.name,
            }
        },
        'creator': {
            'id': task.creator.id,
            'name': task.creator.name,
            'role': {
                'id': task.creator.role.id,
                'name': task.creator.role.name,
            }
        },
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.UnassignUserFromTaskAction')
def test_unassign_user_to_task(mock_action, client, task, tasks):
    task.doer = None
    response = ResponseSuccess(task)
    mock_action().execute.return_value = response

    http_response = client.get('/task/{}/unassign'.format(task.id))

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': task.name,
        'content': task.content,
        'id': task.id,
        'status': {
            'id': task.status.id,
            'name': task.status.name,
        },
        'doer': None,
        'creator': {
            'id': task.creator.id,
            'name': task.creator.name,
            'role': {
                'id': task.creator.role.id,
                'name': task.creator.role.name,
            }
        },
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'
