from taskplus.core.shared.use_case import UseCase
from taskplus.core.shared.response import ResponseSuccess


class DeleteUserRole(UseCase):

    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request):
        user_role_id = request.id
        role = self.repo.delete(user_role_id)
        return ResponseSuccess(role)
