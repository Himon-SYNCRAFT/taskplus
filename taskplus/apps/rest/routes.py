from flask import Blueprint

from taskplus.apps.rest.helpers import json_response
from taskplus.core.use_cases.list_user_roles import ListUserRoles
from taskplus.core.serializers.user_role_serializer import UserRoleEncoder
from taskplus.core.repository.memory.user_roles_memrepo import UserRolesRepo
from taskplus.core.use_cases.list_user_roles_request import ListUserRolesRequest


blueprint = Blueprint('rest', __name__)


@blueprint.route('/roles', methods=['GET'])
def get_all_user_roles():
    request = ListUserRolesRequest.from_dict({})
    repo = UserRolesRepo()
    use_case = ListUserRoles(repo)
    response = use_case.execute(request)

    return json_response(response.value, UserRoleEncoder)
