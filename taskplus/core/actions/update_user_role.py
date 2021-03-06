from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.shared.action import Action
from taskplus.core.shared.request import Request


class UpdateUserRoleAction(Action):

    def __init__(self, repo):
        super().__init__()
        self.repo = repo

    def process_request(self, request):
        role = self.repo.one(id=request.id)

        self._call_before_execution_hooks(dict(request=request, role=role))

        if request.name:
            role.name = request.name

        response = self.repo.update(role)
        self._call_after_execution_hooks(dict(request=request, role=response))

        return ResponseSuccess(response)


class UpdateUserRoleRequest(Request):

    def __init__(self, id, name=None):
        super().__init__()

        self.id = id
        self.name = name

        self._validate()

    def _validate(self):
        self.errors = []

        if not self.id:
            self._add_error('id', 'is required')

        if self.name is not None and not isinstance(self.name, str):
            self._add_error('name', 'expected string, got {}({})'.format(
                self.name.__class__.__name__, self.name
            ))
