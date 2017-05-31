from taskplus.core.domain import Statuses
from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess


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
