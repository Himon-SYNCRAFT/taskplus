from taskplus.core.domain import Statuses
from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.shared.request import Request


class CancelTaskAction(Action):

    def __init__(self, task_repo, status_repo):
        self.task_repo = task_repo
        self.status_repo = status_repo

    def process_request(self, request):
        status = self.status_repo.one(Statuses.CANCELED)

        task_id = request.task_id
        task = self.task_repo.one(task_id)
        task.task_status = status

        response = self.task_repo.update(task)
        return ResponseSuccess(response)


class CancelTaskRequest(Request):

    def __init__(self, task_id):
        super().__init__()
        self.task_id = task_id

    def _validate(self):
        self.errors = []

        if not self.task_id:
            self._add_error('task_id', 'is required')
        elif not isinstance(self.task_id, int):
            self._add_error('task_id', 'expected int, got {}({})'.format(
                self.task_id.__class__.__name__, self.task_id))
