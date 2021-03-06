from taskplus.core.shared.request import Request
from taskplus.core.domain import User
from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess


class AddUserAction(Action):

    def __init__(self, users_repo, roles_repo):
        super().__init__()
        self.users_repo = users_repo
        self.roles_repo = roles_repo

    def process_request(self, request):
        roles = self.roles_repo.list(
            dict(id__in=request.roles))
        user = User(name=request.name, roles=roles)

        self._call_before_execution_hooks(dict(request=request, user=user))
        response = self.users_repo.save(user, password=request.password)
        self._call_after_execution_hooks(dict(request=request, user=response))

        return ResponseSuccess(response)


class AddUserRequest(Request):

    def __init__(self, name, password, roles):
        super().__init__()
        self.name = name
        self.password = password
        self.roles = roles
        self._validate()

    def _validate(self):
        self.errors = []

        if self.name is None:
            self._add_error('name', 'is required')
        elif isinstance(self.name, str) and not self.name.strip():
            self._add_error('name', 'is required')
        elif not isinstance(self.name, str):
            message = 'expected str, got {}({})'.format(
                self.name.__class__.__name__, self.name
            )
            self._add_error('name', message)

        if self.password is None:
            self._add_error('password', 'is required')
        elif isinstance(self.password, str) and not self.password.strip():
            self._add_error('password', 'is required')
        elif not isinstance(self.password, str):
            message = 'expected str, got {}({})'.format(
                self.password.__class__.__name__, self.password
            )
            self._add_error('password', message)

        if not self.roles:
            self._add_error('roles', 'is required')
        elif not isinstance(self.roles, list):
            message = 'expected list, got {}({})'.format(
                self.roles.__class__.__name__, self.roles
            )
            self._add_error('roles', message)
        else:
            for index, role in enumerate(self.roles):
                if not isinstance(role, int):
                    err = 'expected all elements to be int, got {}({}) at index {}'
                    message = err.format(
                        role.__class__.__name__, role, index
                    )
                    self._add_error('roles', message)
