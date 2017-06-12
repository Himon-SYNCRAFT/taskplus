from taskplus.core.shared.request import Request
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


class AddUserRoleRequest(Request):

    def __init__(self, name):
        super().__init__()
        self.name = name
        self._validate()

    def _validate(self):
        self.errors = []

        if self.name is None:
            self._add_error('name', 'is required')
        elif isinstance(self.name, str) and not self.name.strip():
            self._add_error('name', 'is required')
        elif not isinstance(self.name, str):
            message = 'expected string, got {}({})'.format(
                self.name.__class__.__name__, self.name
            )
            self._add_error('name', message)
