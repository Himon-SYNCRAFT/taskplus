from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess


class DeleteUserRoleAction(Action):

    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request):
        user_role_id = request.id
        role = self.repo.delete(user_role_id)
        return ResponseSuccess(role)
