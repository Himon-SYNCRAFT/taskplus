from taskplus.core.shared.action import Action
from taskplus.core.shared.request import Request
from taskplus.core.shared.response import ResponseSuccess


class UpdateTaskStatusAction(Action):

    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request):
        status = self.repo.one(id=request.id)

        if request.name:
            status.name = request.name

        self.repo.update(status)
        return ResponseSuccess(status)


class UpdateTaskStatusRequest(Request):

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
