from taskplus.core.shared.action import Action
from taskplus.core.shared.request import Request
from taskplus.core.shared.response import ResponseSuccess


class DeleteTaskStatusAction(Action):

    def __init__(self, repo):
        super().__init__()
        self.statuses_repo = repo

    def process_request(self, request):
        self._call_before_execution_hooks(request, None)
        status_id = request.id
        status = self.statuses_repo.delete(status_id)
        self._call_after_execution_hooks(request, status)

        return ResponseSuccess(status)


class DeleteTaskStatusRequest(Request):

    def __init__(self, id):
        super().__init__()
        self.id = id
        self._validate()

    def _validate(self):
        self.errors = []

        if not self.id:
            self._add_error('id', 'is required')
