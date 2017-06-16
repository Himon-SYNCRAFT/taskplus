from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.shared.request import Request


class UpdateUserAction(Action):

    def __init__(self, repo):
        super().__init__()
        self.repo = repo

    def process_request(self, request):
        user_id = request.id
        user = self.repo.one(user_id)

        self._call_before_execution_hooks(request, user)

        if request.name:
            user.name = request.name

        if request.role_id:
            user.role.id = request.role_id

        response = self.repo.update(user)
        self._call_after_execution_hooks(request, response)

        return ResponseSuccess(response)


class UpdateUserRequest(Request):

    def __init__(self, id, name=None, role_id=None):
        super().__init__()

        self.id = id
        self.name = name
        self.role_id = role_id

        self._validate()

    def _validate(self):
        self.errors = []

        if self.id is None:
            self._add_error('id', 'is required')
        elif not isinstance(self.id, int):
            self._add_error('id', 'expected int, got {}({})'.format(
                self.id.__class__.__name__, self.id))

        if self.name is not None and not isinstance(self.name, str):
            self._add_error('name', 'expected str, got {}({})'.format(
                self.name.__class__.__name__, self.name))

        if self.role_id is not None and not isinstance(self.role_id, int):
            self._add_error('role_id', 'expected int, got {}({})'.format(
                self.role_id.__class__.__name__, self.role_id))
