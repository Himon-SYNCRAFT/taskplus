from flask import Blueprint
from flask import request as http_request

from taskplus.apps.rest.helpers import json_response
from taskplus.apps.rest.repositories import UserRolesRepository
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
    UpdateTaskStatusAction, UpdateTaskStatusRequest
)
from taskplus.core.serializers.user_role_serializer import UserRoleEncoder


blueprint = Blueprint('rest', __name__)
user_roles_repository = UserRolesRepository()


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
    action = ListUserRolesAction(user_roles_repository)
    response = action.execute(request)

    return json_response(response.value, UserRoleEncoder)
