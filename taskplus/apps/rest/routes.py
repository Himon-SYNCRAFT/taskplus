from flask import Blueprint
from flask import request as http_request

from taskplus.apps.rest.helpers import json_response
from taskplus.apps.rest.repositories import (UserRolesRepository,
                                             TaskStatusesRepository,
                                             UsersRepository)
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
)
from taskplus.core.serializers.user_role_serializer import UserRoleEncoder
from taskplus.core.serializers.task_status_serializer import TaskStatusEncoder
from taskplus.core.serializers.user_serializer import UserEncoder


blueprint = Blueprint('rest', __name__)
user_roles_repository = UserRolesRepository()
task_statuses_repository = TaskStatusesRepository()
users_repository = UsersRepository()


@blueprint.route('/roles', methods=['GET'])
def get_all_user_roles():
    request = ListUserRolesRequest()
    action = ListUserRolesAction(user_roles_repository)
    response = action.execute(request)

    return json_response(response.value, UserRoleEncoder)


@blueprint.route('/role/<int:id>', methods=['GET'])
def get_user_role_details(id):
    request = GetRoleDetailsRequest(id)
    action = GetRoleDetailsAction(user_roles_repository)
    response = action.execute(request)

    return json_response(response.value, UserRoleEncoder)


@blueprint.route('/role', methods=['POST'])
def add_user_role():
    data = http_request.get_json()
    request = AddUserRoleRequest(**data)
    action = AddUserRoleAction(user_roles_repository)
    response = action.execute(request)

    return json_response(response.value, UserRoleEncoder)


@blueprint.route('/role/<int:id>', methods=['DELETE'])
def delete_user_role(id):
    request = DeleteUserRoleRequest(id)
    action = DeleteUserRoleAction(user_roles_repository)
    response = action.execute(request)

    return json_response(response.value, UserRoleEncoder)


@blueprint.route('/role', methods=['PUT'])
def update_user_role():
    data = http_request.get_json()
    request = UpdateUserRoleRequest(**data)
    action = UpdateUserRoleAction(user_roles_repository)
    response = action.execute(request)

    return json_response(response.value, UserRoleEncoder)


@blueprint.route('/statuses', methods=['GET'])
def get_all_task_statuses():
    request = ListTaskStatusesRequest()
    action = ListTaskStatusesAction(task_statuses_repository)
    response = action.execute(request)

    return json_response(response.value, TaskStatusEncoder)


@blueprint.route('/status/<int:id>', methods=['GET'])
def get_task_status_details(id):
    request = GetTaskStatusDetailsRequest(id)
    action = GetTaskStatusDetailsAction(task_statuses_repository)
    response = action.execute(request)

    return json_response(response.value, TaskStatusEncoder)


@blueprint.route('/status', methods=['POST'])
def add_task_status():
    data = http_request.get_json()
    request = AddTaskStatusRequest(**data)
    action = AddTaskStatusAction(task_statuses_repository)
    response = action.execute(request)

    return json_response(response.value, TaskStatusEncoder)


@blueprint.route('/status/<int:id>', methods=['DELETE'])
def delete_task_status(id):
    request = DeleteTaskStatusRequest(id)
    action = DeleteTaskStatusAction(task_statuses_repository)
    response = action.execute(request)

    return json_response(response.value, TaskStatusEncoder)


@blueprint.route('/status', methods=['PUT'])
def update_task_status():
    data = http_request.get_json()
    request = UpdateTaskStatusRequest(**data)
    action = UpdateTaskStatusAction(task_statuses_repository)
    response = action.execute(request)

    return json_response(response.value, TaskStatusEncoder)


@blueprint.route('/users', methods=['GET'])
def get_all_users():
    request = ListUsersRequest()
    action = ListUsersAction(users_repository)
    response = action.execute(request)

    return json_response(response.value, UserEncoder)


@blueprint.route('/user/<int:id>', methods=['GET'])
def get_user_details(id):
    request = GetUserDetailsRequest(id)
    action = GetUserDetailsAction(users_repository)
    response = action.execute(request)

    return json_response(response.value, UserEncoder)


@blueprint.route('/user', methods=['POST'])
def add_user():
    data = http_request.get_json()
    request = AddUserRequest(
        name=data['name'],
        role_id=data['role_id'],
    )
    action = AddUserAction(users_repository, user_roles_repository)
    response = action.execute(request)

    return json_response(response.value, UserEncoder)


@blueprint.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    request = DeleteUserRequest(id)
    action = DeleteUserAction(users_repository)
    response = action.execute(request)

    return json_response(response.value, UserEncoder)


@blueprint.route('/user', methods=['PUT'])
def update_user():
    data = http_request.get_json()
    request = UpdateUserRequest(**data)
    action = UpdateUserAction(users_repository)
    response = action.execute(request)

    return json_response(response.value, UserEncoder)
