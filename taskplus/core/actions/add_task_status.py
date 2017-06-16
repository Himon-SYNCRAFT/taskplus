from taskplus.core.domain import TaskStatus
from taskplus.core.shared.action import Action
from taskplus.core.shared.request import Request
from taskplus.core.shared.response import ResponseSuccess


class AddTaskStatusAction(Action):

    def __init__(self, statuses_repo):
        super().__init__()
        self.statuses_repo = statuses_repo

    def process_request(self, request):
        self._call_before_execution_hooks(request, None)

        new_status = TaskStatus(name=request.name)
        response = self.statuses_repo.save(new_status)

        self._call_after_execution_hooks(request, response)

        return ResponseSuccess(response)


class AddTaskStatusRequest(Request):

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
