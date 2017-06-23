from taskplus.core.domain import Statuses
from taskplus.core.shared.action import Action
from taskplus.core.shared.request import Request
from taskplus.core.shared.response import ResponseSuccess


class GetNotCompletedTasksAction(Action):

    def __init__(self, task_repo):
        super().__init__()
        self.task_repo = task_repo

    def process_request(self, request):
        self._call_before_execution_hooks(dict(request=request, tasks=None))
        response = self.task_repo.list(filters=request.filters)
        self._call_after_execution_hooks(dict(request=request, tasks=response))

        return ResponseSuccess(response)


class GetNotCompletedTasksRequest(Request):
    def __init__(self):
        super().__init__()
        self.filters = {
            'status_id__notin': [
                Statuses.CANCELED,
                Statuses.COMPLETED
            ]
        }

    def _validate(self):
        pass
