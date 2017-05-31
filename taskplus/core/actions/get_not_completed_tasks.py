from taskplus.core.domain import Statuses
from taskplus.core.shared.action import Action
from taskplus.core.shared.request import Request
from taskplus.core.shared.response import ResponseSuccess


class GetNotCompletedTasksRequest(Request):
    def __init__(self):
        super().__init__()
        self.filters = {
            'status_id__notin': [
                Statuses.CANCELED.value,
                Statuses.COMPLETED.value
            ]
        }

    def _validate(self):
        pass


class GetNotCompletedTasksAction(Action):
    def __init__(self, task_repo):
        self.task_repo = task_repo

    def process_request(self, request):
        print(request.filters)
        response = self.task_repo.list(filters=request.filters)
        return ResponseSuccess(response)
