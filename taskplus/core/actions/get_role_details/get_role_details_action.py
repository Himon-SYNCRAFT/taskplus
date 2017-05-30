from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess


class GetRoleDetailsAction(Action):

    def __init__(self, roles_repo):
        self.roles_repo = roles_repo

    def process_request(self, request):
        role = self.roles_repo.one(request.role_id)
        return ResponseSuccess(role)
