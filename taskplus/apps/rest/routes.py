import flask_login
from flask_login import login_required
from flask import Blueprint, jsonify
from flask import request as http_request

from taskplus.apps.rest.helpers import json_response
from taskplus.apps.rest.repositories import (UserRolesRepository,
                                             TaskStatusesRepository,
                                             UsersRepository,
                                             TasksRepository)
from taskplus.core.actions import (
    ListUserRolesAction, ListUserRolesRequest,
    GetRoleDetailsAction, GetRoleDetailsRequest,
    DeleteUserRoleAction, DeleteUserRoleRequest,
    AddUserRoleAction, AddUserRoleRequest,
    UpdateUserRoleAction, UpdateUserRoleRequest,
    ListTaskStatusesAction, ListTaskStatusesRequest,
    GetTaskStatusDetailsAction, GetTaskStatusDetailsRequest,
    DeleteTaskStatusAction, DeleteTaskStatusRequest,
    AddTaskStatusAction, AddTaskStatusRequest,
    UpdateTaskStatusAction, UpdateTaskStatusRequest,
    ListUsersAction, ListUsersRequest,
    GetUserDetailsAction, GetUserDetailsRequest,
    DeleteUserAction, DeleteUserRequest,
    AddUserAction, AddUserRequest,
    UpdateUserAction, UpdateUserRequest,
    ListTasksAction, ListTasksRequest,
    GetNotCompletedTasksAction, GetNotCompletedTasksRequest,
    GetTaskDetailsAction, GetTaskDetailsRequest,
    CancelTaskAction, CancelTaskRequest,
    CompleteTaskAction, CompleteTaskRequest,
    AssignUserToTaskAction, AssignUserToTaskRequest,
    UnassignUserFromTaskAction, UnassignUserFromTaskRequest,
    AddTaskAction, AddTaskRequest,
)
from taskplus.core.serializers.user_role_serializer import UserRoleEncoder
from taskplus.core.serializers.task_status_serializer import TaskStatusEncoder
from taskplus.core.serializers.user_serializer import UserEncoder
from taskplus.core.serializers.task_serializer import TaskEncoder


blueprint = Blueprint('rest', __name__)
user_roles_repository = UserRolesRepository()
task_statuses_repository = TaskStatusesRepository()
users_repository = UsersRepository()
tasks_repository = TasksRepository()


@blueprint.route('/auth/login', methods=['POST'])
def login():
    data = http_request.get_json()
    name = data['name']
    password = data['password']
    request = ListUsersRequest(filters=dict(name=name))
    action = ListUsersAction(users_repository)
    response = action.execute(request)

    if not response or not response.value:
        message = 'Login failed. User with name {} not found.'.format(name)
        return jsonify(dict(message=message)), 401

    user = response.value[0]

    if not users_repository.check_password(user, password):
        message = 'Login failed. Invalid password.'
        return jsonify(dict(message=message)), 401

    user.is_active = True
    user.is_authenticated = True
    user.is_anonymous = False

    def get_id():
        return user.name

    user.get_id = get_id

    flask_login.login_user(user)
    return json_response(response.value[0], UserEncoder)


@blueprint.route('/auth/logout', methods=['GET'])
def logout():
    flask_login.logout_user()
    message = 'Logged out'
    return jsonify(dict(message=message)), 200


@blueprint.route('/roles', methods=['GET'])
@login_required
def get_all_user_roles():
    request = ListUserRolesRequest()
    action = ListUserRolesAction(user_roles_repository)
    response = action.execute(request)

    return json_response(response.value, UserRoleEncoder)


@blueprint.route('/roles', methods=['POST'])
@login_required
def get_user_roles_by():
    data = http_request.get_json()
    request = ListUserRolesRequest(**data)
    action = ListUserRolesAction(user_roles_repository)
    response = action.execute(request)

    return json_response(response.value, UserRoleEncoder)


@blueprint.route('/role/<int:id>', methods=['GET'])
@login_required
def get_user_role_details(id):
    request = GetRoleDetailsRequest(id)
    action = GetRoleDetailsAction(user_roles_repository)
    response = action.execute(request)

    return json_response(response.value, UserRoleEncoder)


@blueprint.route('/role', methods=['POST'])
@login_required
def add_user_role():
    data = http_request.get_json()
    request = AddUserRoleRequest(**data)
    action = AddUserRoleAction(user_roles_repository)
    response = action.execute(request)

    return json_response(response.value, UserRoleEncoder)


@blueprint.route('/role/<int:id>', methods=['DELETE'])
@login_required
def delete_user_role(id):
    request = DeleteUserRoleRequest(id)
    action = DeleteUserRoleAction(user_roles_repository)
    response = action.execute(request)

    return json_response(response.value, UserRoleEncoder)


@blueprint.route('/role', methods=['PUT'])
@login_required
def update_user_role():
    data = http_request.get_json()
    request = UpdateUserRoleRequest(**data)
    action = UpdateUserRoleAction(user_roles_repository)
    response = action.execute(request)

    return json_response(response.value, UserRoleEncoder)


@blueprint.route('/statuses', methods=['GET'])
@login_required
def get_all_task_statuses():
    request = ListTaskStatusesRequest()
    action = ListTaskStatusesAction(task_statuses_repository)
    response = action.execute(request)

    return json_response(response.value, TaskStatusEncoder)


@blueprint.route('/statuses', methods=['POST'])
@login_required
def get_task_statuses_by():
    data = http_request.get_json()
    request = ListTaskStatusesRequest(**data)
    action = ListTaskStatusesAction(task_statuses_repository)
    response = action.execute(request)

    return json_response(response.value, TaskStatusEncoder)


@blueprint.route('/status/<int:id>', methods=['GET'])
@login_required
def get_task_status_details(id):
    request = GetTaskStatusDetailsRequest(id)
    action = GetTaskStatusDetailsAction(task_statuses_repository)
    response = action.execute(request)

    return json_response(response.value, TaskStatusEncoder)


@blueprint.route('/status', methods=['POST'])
@login_required
def add_task_status():
    data = http_request.get_json()
    request = AddTaskStatusRequest(**data)
    action = AddTaskStatusAction(task_statuses_repository)
    response = action.execute(request)

    return json_response(response.value, TaskStatusEncoder)


@blueprint.route('/status/<int:id>', methods=['DELETE'])
@login_required
def delete_task_status(id):
    request = DeleteTaskStatusRequest(id)
    action = DeleteTaskStatusAction(task_statuses_repository)
    response = action.execute(request)

    return json_response(response.value, TaskStatusEncoder)


@blueprint.route('/status', methods=['PUT'])
@login_required
def update_task_status():
    data = http_request.get_json()
    request = UpdateTaskStatusRequest(**data)
    action = UpdateTaskStatusAction(task_statuses_repository)
    response = action.execute(request)

    return json_response(response.value, TaskStatusEncoder)


@blueprint.route('/users', methods=['GET'])
@login_required
def get_all_users():
    request = ListUsersRequest()
    action = ListUsersAction(users_repository)
    response = action.execute(request)

    return json_response(response.value, UserEncoder)


@blueprint.route('/users', methods=['POST'])
@login_required
def get_users_by():
    data = http_request.get_json()
    request = ListUsersRequest(**data)
    action = ListUsersAction(users_repository)
    response = action.execute(request)

    return json_response(response.value, UserEncoder)


@blueprint.route('/user/<int:id>', methods=['GET'])
@login_required
def get_user_details(id):
    request = GetUserDetailsRequest(id)
    action = GetUserDetailsAction(users_repository)
    response = action.execute(request)

    return json_response(response.value, UserEncoder)


@blueprint.route('/user', methods=['POST'])
@login_required
def add_user():
    data = http_request.get_json()
    request = AddUserRequest(**data)
    action = AddUserAction(users_repository, user_roles_repository)
    response = action.execute(request)

    return json_response(response.value, UserEncoder)


@blueprint.route('/user/<int:id>', methods=['DELETE'])
@login_required
def delete_user(id):
    request = DeleteUserRequest(id)
    action = DeleteUserAction(users_repository)
    response = action.execute(request)

    return json_response(response.value, UserEncoder)


@blueprint.route('/user', methods=['PUT'])
@login_required
def update_user():
    data = http_request.get_json()
    request = UpdateUserRequest(**data)
    action = UpdateUserAction(users_repository)
    response = action.execute(request)

    return json_response(response.value, UserEncoder)


@blueprint.route('/tasks', methods=['GET'])
@login_required
def get_all_tasks():
    request = ListTasksRequest()
    action = ListTasksAction(tasks_repository)
    response = action.execute(request)

    return json_response(response.value, TaskEncoder)


@blueprint.route('/tasks/notcompleted', methods=['GET'])
@login_required
def get_not_completed_tasks():
    request = GetNotCompletedTasksRequest()
    action = GetNotCompletedTasksAction(tasks_repository)
    response = action.execute(request)

    return json_response(response.value, TaskEncoder)


@blueprint.route('/tasks', methods=['POST'])
@login_required
def get_tasks_by():
    data = http_request.get_json()
    request = ListTasksRequest(**data)
    action = ListTasksAction(tasks_repository)
    response = action.execute(request)

    return json_response(response.value, TaskEncoder)


@blueprint.route('/task/<int:id>', methods=['GET'])
@login_required
def get_task_details(id):
    request = GetTaskDetailsRequest(id)
    action = GetTaskDetailsAction(tasks_repository)
    response = action.execute(request)

    return json_response(response.value, TaskEncoder)


@blueprint.route('/task', methods=['POST'])
@login_required
def add_task():
    data = http_request.get_json()
    request = AddTaskRequest(**data)
    action = AddTaskAction(tasks_repository)
    response = action.execute(request)

    return json_response(response.value, TaskEncoder)


@blueprint.route('/task/<int:id>/cancel', methods=['GET'])
@login_required
def cancel_task(id):
    request = CancelTaskRequest(id)
    action = CancelTaskAction(tasks_repository)
    response = action.execute(request)

    return json_response(response.value, TaskEncoder)


@blueprint.route('/task/<int:id>/complete', methods=['GET'])
@login_required
def complete_task(id):
    request = CompleteTaskRequest(id)
    action = CompleteTaskAction(tasks_repository)
    response = action.execute(request)

    return json_response(response.value, TaskEncoder)


@blueprint.route('/task/<int:task_id>/assign/<int:user_id>', methods=['GET'])
@login_required
def assing_user_to_task(task_id, user_id):
    request = AssignUserToTaskRequest(task_id=task_id, user_id=user_id)
    action = AssignUserToTaskAction(tasks_repository)
    response = action.execute(request)

    return json_response(response.value, TaskEncoder)


@blueprint.route('/task/<int:task_id>/unassign', methods=['GET'])
@login_required
def unassing_user_from_task(task_id):
    request = UnassignUserFromTaskRequest(task_id=task_id)
    action = UnassignUserFromTaskAction(tasks_repository)
    response = action.execute(request)

    return json_response(response.value, TaskEncoder)
