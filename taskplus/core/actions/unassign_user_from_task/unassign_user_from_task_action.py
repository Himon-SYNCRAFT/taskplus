from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.shared.action import Action


class UnassignUserFromTaskAction(Action):

    def __init__(self, tasks_repo):
        self.tasks_repo = tasks_repo

    def process_request(self, request):
        task_id = request.task_id
        task = self.tasks_repo.get(task_id)

        task.doer = None
        response = self.tasks_repo.update(task)

        return ResponseSuccess(response)
