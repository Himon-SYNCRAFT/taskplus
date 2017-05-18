from taskplus.core.domain import UserRole
from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess


class AddUserRoleAction(Action):

    def __init__(self, roles_repo):
        self.roles_repo = roles_repo

    def process_request(self, request):
        new_role = UserRole(name=request.name)
        response = self.roles_repo.save(new_role)
        return ResponseSuccess(response)
