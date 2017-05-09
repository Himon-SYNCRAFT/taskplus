from taskplus.core.shared.action import Action
from taskplus.core.domain.user_role import UserRole
from taskplus.core.shared.response import ResponseSuccess


class AddUserRoleAction(Action):

    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request):
        new_role = UserRole(name=request.name)
        self.repo.save(new_role)
        return ResponseSuccess(new_role)
