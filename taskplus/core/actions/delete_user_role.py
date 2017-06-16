from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.shared.request import Request


class DeleteUserRoleAction(Action):

    def __init__(self, repo):
        super().__init__()
        self.repo = repo

    def process_request(self, request):
        user_role_id = request.id

        self._call_before_execution_hooks(request, None)
        role = self.repo.delete(user_role_id)
        self._call_after_execution_hooks(request, role)

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
