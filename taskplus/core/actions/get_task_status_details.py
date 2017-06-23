from taskplus.core.shared.action import Action
from taskplus.core.shared.request import Request
from taskplus.core.shared.response import ResponseSuccess


class GetTaskStatusDetailsAction(Action):

    def __init__(self, statuses_repo):
        super().__init__()
        self.statuses_repo = statuses_repo

    def process_request(self, request):
        self._call_before_execution_hooks(dict(request=request, status=None))
        status = self.statuses_repo.one(request.status_id)
        self._call_after_execution_hooks(dict(request=request, status=status))

        return ResponseSuccess(status)


class GetTaskStatusDetailsRequest(Request):

    def __init__(self, status_id):
        super().__init__()
        self.status_id = status_id

    def _validate(self):
        self.errors = []

        if not self.status_id:
            self._add_error('status_id', 'is required')
        elif not isinstance(self.status_id, int):
            self._add_error('status_id', 'expected int, got {}({})'.format(
                self.status_id.__class__.__name__, self.status_id
            ))
