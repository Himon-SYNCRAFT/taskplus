from flask import Blueprint

from taskplus.apps.rest.helpers import json_response
from taskplus.core.actions import ListUserRolesAction
from taskplus.core.actions import ListUserRolesRequest
from taskplus.core.repository.memory.user_roles_memrepo import UserRolesRepo
from taskplus.core.serializers.user_role_serializer import UserRoleEncoder


blueprint = Blueprint('rest', __name__)


@blueprint.route('/roles', methods=['GET'])
def get_all_user_roles():
    request = ListUserRolesRequest()
    repo = UserRolesRepo()
    action = ListUserRolesAction(repo)
    response = action.execute(request)

    return json_response(response.value, UserRoleEncoder)
