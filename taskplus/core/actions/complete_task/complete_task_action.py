from taskplus.core.domain import Statuses
from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.shared.action import Action


class CompleteTaskAction(Action):

    def __init__(self, task_repo, status_repo):
        self.task_repo = task_repo
        self.status_repo = status_repo

    def process_request(self, request):
        task_id = request.task_id
        status = self.status_repo.get(Statuses.COMPLETED)
        task = self.task_repo.get(task_id)
        task.status = status

        response = self.task_repo.update(task)
        return ResponseSuccess(response)
