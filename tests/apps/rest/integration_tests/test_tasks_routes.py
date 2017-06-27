import json
from sqlalchemy import event
from sqlalchemy.engine import Engine
from collections import namedtuple
from unittest import mock

from taskplus.core.domain import Statuses
from taskplus.apps.rest.repositories import UsersRepository
from taskplus.apps.rest.routes import authorization_manager
from taskplus.apps.rest.database import Base, db_session, engine


users_repository = UsersRepository()

User = namedtuple('User', ['id', 'name', 'roles'])
Role = namedtuple('Role', ['id', 'name'])
Task = namedtuple('Task', ['id', 'name', 'content', 'status', 'creator', 'doer'])
Status = namedtuple('Status', ['id', 'name'])

user = User(id=1, name='super', roles=[
    Role(id=1, name='creator'),
    Role(id=2, name='doer'),
    Role(id=3, name='admin'),
])

user2 = User(id=2, name='user2', roles=[
    Role(id=1, name='creator'),
    Role(id=2, name='doer'),
    Role(id=3, name='admin'),
])

task = Task(id=1, name='task1', content='lorem ipsum',
            status=Status(id=1, name='new'), creator=user, doer=user2)

task2 = Task(id=2, name='task2', content='lorem ipsum',
             status=Status(id=1, name='new'), creator=user2, doer=user)

task3 = Task(id=3, name='task3', content='lorem ipsum',
             status=Status(id=1, name='new'), creator=user2, doer=None)


def setup_function(function):
    if db_session.bind.driver == 'pysqlite':
        @event.listens_for(Engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    from taskplus.apps.rest import models
    Base.metadata.reflect(engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    roles = [models.UserRole(name=role.name, id=role.id) for role in user.roles]

    for role in roles:
        db_session.add(role)

    db_session.commit()

    db_session.add(models.User(
        id=user.id,
        name=user.name,
        roles=roles,
        password='super'
    ))

    db_session.add(models.User(
        id=user2.id,
        name=user2.name,
        roles=roles,
        password='user2'
    ))

    db_session.commit()

    status_new = models.TaskStatus(id=Statuses.NEW, name='new')
    status_in_progress = models.TaskStatus(
        id=Statuses.IN_PROGRESS, name='in progress')
    status_completed = models.TaskStatus(
        id=Statuses.COMPLETED, name='completed')
    status_canceled = models.TaskStatus(
        id=Statuses.CANCELED, name='canceled')

    db_session.add(status_new)
    db_session.add(status_in_progress)
    db_session.add(status_completed)
    db_session.add(status_canceled)
    db_session.commit()

    db_session.add(models.Task(
        id=task.id,
        name=task.name,
        content=task.content,
        status_id=task.status.id,
        creator_id=task.creator.id,
        doer_id=task.doer.id
    ))

    db_session.add(models.Task(
        id=task2.id,
        name=task2.name,
        content=task2.content,
        status_id=task2.status.id,
        creator_id=task2.creator.id,
        doer_id=task2.doer.id
    ))

    db_session.add(models.Task(
        id=task3.id,
        name=task3.name,
        content=task3.content,
        status_id=task3.status.id,
        creator_id=task3.creator.id,
    ))

    db_session.commit()

    user_ = users_repository.one(1)
    authorization_manager.user = user_


def test_get_tasks_list(client):
    http_response = client.get('/tasks')
    doer_roles = [{'id': role.id, 'name': role.name} for role in task.doer.roles]
    creator_roles = [
        {'id': role.id, 'name': role.name} for role in task.creator.roles]

    assert json.loads(http_response.data.decode('UTF-8')) == [
        {
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
                'roles': doer_roles
            },
            'creator': {
                'id': task.creator.id,
                'name': task.creator.name,
                'roles': creator_roles
            },
        },
        {
            'name': task2.name,
            'content': task2.content,
            'id': task2.id,
            'status': {
                'id': task2.status.id,
                'name': task2.status.name,
            },
            'doer': {
                'id': task2.doer.id,
                'name': task2.doer.name,
                'roles': doer_roles
            },
            'creator': {
                'id': task2.creator.id,
                'name': task2.creator.name,
                'roles': creator_roles
            },
        },
        {
            'name': task3.name,
            'content': task3.content,
            'id': task3.id,
            'status': {
                'id': task3.status.id,
                'name': task3.status.name,
            },
            'doer': None,
            'creator': {
                'id': task3.creator.id,
                'name': task3.creator.name,
                'roles': creator_roles
            },
        }
    ]

    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_get_not_completed_tasks(client):
    http_response = client.get('/tasks/notcompleted')
    doer_roles = [
        {'id': role.id, 'name': role.name} for role in task.doer.roles]
    creator_roles = [
        {'id': role.id, 'name': role.name} for role in task.creator.roles]

    assert json.loads(http_response.data.decode('UTF-8')) == [
        {
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
                'roles': doer_roles
            },
            'creator': {
                'id': task.creator.id,
                'name': task.creator.name,
                'roles': creator_roles
            },
        },
        {
            'name': task2.name,
            'content': task2.content,
            'id': task2.id,
            'status': {
                'id': task2.status.id,
                'name': task2.status.name,
            },
            'doer': {
                'id': task2.doer.id,
                'name': task2.doer.name,
                'roles': doer_roles
            },
            'creator': {
                'id': task2.creator.id,
                'name': task2.creator.name,
                'roles': creator_roles
            },
        },
        {
            'name': task3.name,
            'content': task3.content,
            'id': task3.id,
            'status': {
                'id': task3.status.id,
                'name': task3.status.name,
            },
            'doer': None,
            'creator': {
                'id': task3.creator.id,
                'name': task3.creator.name,
                'roles': creator_roles
            },
        }
    ]
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_get_tasks_list_with_filters(client):
    data = json.dumps(dict(filters=dict(name=task.name)))
    http_response = client.post('/tasks', data=data,
                                content_type='application/json')
    doer_roles = [
        {'id': role.id, 'name': role.name} for role in task.doer.roles]
    creator_roles = [
        {'id': role.id, 'name': role.name} for role in task.creator.roles]

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
            'roles': doer_roles
        },
        'creator': {
            'id': task.creator.id,
            'name': task.creator.name,
            'roles': creator_roles
        },
    }]
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_get_task_details(client):
    http_response = client.get('/task/{}'.format(task.id))
    doer_roles = [
        {'id': role.id, 'name': role.name} for role in task.doer.roles]
    creator_roles = [
        {'id': role.id, 'name': role.name} for role in task.creator.roles]

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
            'roles': doer_roles
        },
        'creator': {
            'id': task.creator.id,
            'name': task.creator.name,
            'roles': creator_roles
        },
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_add_task(client):
    data = json.dumps(dict(name=task.name, content='lorem ipsum',
                           creator_id=task.creator.id))
    http_response = client.post('/task', data=data,
                                content_type='application/json')
    creator_roles = [
        {'id': role.id, 'name': role.name} for role in task.creator.roles]

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': task.name,
        'content': task.content,
        'id': 4,
        'status': {
            'id': 1,
            'name': 'new',
        },
        'doer': None,
        'creator': {
            'id': task.creator.id,
            'name': task.creator.name,
            'roles': creator_roles
        },
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_update_task(client):
    name = 'asdfsdf'
    content = 'wajrksdfs'
    data = json.dumps(dict(name=name, content=content))
    http_response = client.put('/task/{}'.format(task.id), data=data,
                               content_type='application/json')
    creator_roles = [
        {'id': role.id, 'name': role.name} for role in task.creator.roles]
    doer_roles = [
        {'id': role.id, 'name': role.name} for role in task.doer.roles]

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': name,
        'content': content,
        'id': task.id,
        'status': {
            'id': task.status.id,
            'name': task.status.name,
        },
        'doer': {
            'id': task.doer.id,
            'name': task.doer.name,
            'roles': doer_roles
        },
        'creator': {
            'id': task.creator.id,
            'name': task.creator.name,
            'roles': creator_roles
        },
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_cancel_task(client):
    task_status = Status(id=Statuses.CANCELED, name='canceled')
    task = task2

    http_response = client.get('/task/{}/cancel'.format(task.id))
    doer_roles = [{'id': role.id, 'name': role.name} for role in task.doer.roles]
    creator_roles = [
        {'id': role.id, 'name': role.name} for role in task.creator.roles]

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': task.name,
        'content': task.content,
        'id': task.id,
        'status': {
            'id': task_status.id,
            'name': task_status.name,
        },
        'doer': {
            'id': task.doer.id,
            'name': task.doer.name,
            'roles': doer_roles
        },
        'creator': {
            'id': task.creator.id,
            'name': task.creator.name,
            'roles': creator_roles
        },
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_completed_task(client):
    task_status = Status(id=Statuses.COMPLETED, name='completed')
    task = task2

    http_response = client.get('/task/{}/complete'.format(task.id))
    doer_roles = [{'id': role.id, 'name': role.name} for role in task.doer.roles]
    creator_roles = [
        {'id': role.id, 'name': role.name} for role in task.creator.roles]

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': task.name,
        'content': task.content,
        'id': task.id,
        'status': {
            'id': task_status.id,
            'name': task_status.name,
        },
        'doer': {
            'id': task.doer.id,
            'name': task.doer.name,
            'roles': doer_roles
        },
        'creator': {
            'id': task.creator.id,
            'name': task.creator.name,
            'roles': creator_roles
        },
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('taskplus.apps.rest.routes.current_user')
def test_assign_user_to_task(current_user, client):
    user_ = users_repository.one(1)
    current_user.id = 1
    current_user.permissions = user_.permissions

    task_doer = User(
        id=user.id, name=user.name, roles=[role for role in user.roles])

    http_response = client.get(
        '/task/{}/assign'.format(task3.id, task_doer.id))
    doer_roles = [{'id': role.id, 'name': role.name} for role in task_doer.roles]
    creator_roles = [
        {'id': role.id, 'name': role.name} for role in task.creator.roles]

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': task3.name,
        'content': task3.content,
        'id': task3.id,
        'status': {
            'id': task3.status.id,
            'name': task3.status.name,
        },
        'doer': {
            'id': task_doer.id,
            'name': task_doer.name,
            'roles': doer_roles
        },
        'creator': {
            'id': task3.creator.id,
            'name': task3.creator.name,
            'roles': creator_roles
        },
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


def test_unassign_user_to_task(client):
    http_response = client.get('/task/{}/unassign'.format(task2.id))
    creator_roles = [
        {'id': role.id, 'name': role.name} for role in task2.creator.roles]

    assert json.loads(http_response.data.decode('UTF-8')) == {
        'name': task2.name,
        'content': task2.content,
        'id': task2.id,
        'status': {
            'id': task2.status.id,
            'name': task2.status.name,
        },
        'doer': None,
        'creator': {
            'id': task2.creator.id,
            'name': task2.creator.name,
            'roles': creator_roles
        },
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'
