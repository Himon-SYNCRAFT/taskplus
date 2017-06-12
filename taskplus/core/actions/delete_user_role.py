from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.shared.request import Request


class DeleteUserRoleAction(Action):

    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request):
        user_role_id = request.id
        role = self.repo.delete(user_role_id)
        return ResponseSuccess(role)


class DeleteUserRoleRequest(Request):

    def __init__(self, id):
        super().__init__()
        self.id = id
        self._validate()

    def _validate(self):
        self.errors = []

        if not self.id:
            self._add_error('id', 'is required')
