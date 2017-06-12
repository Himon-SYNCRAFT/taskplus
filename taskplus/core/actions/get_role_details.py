from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.shared.request import Request


class GetRoleDetailsAction(Action):

    def __init__(self, roles_repo):
        self.roles_repo = roles_repo

    def process_request(self, request):
        role = self.roles_repo.one(request.role_id)
        return ResponseSuccess(role)


class GetRoleDetailsRequest(Request):

    def __init__(self, role_id):
        super().__init__()
        self.role_id = role_id

    def _validate(self):
        self.errors = []

        if not self.role_id:
            self._add_error('role_id', 'is required')
        elif not isinstance(self.role_id, int):
            self._add_error('role_id', 'expected int, got {}({})'.format(
                self.role_id.__class__.__name__, self.role_id
            ))
