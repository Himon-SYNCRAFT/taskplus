from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess


class GetTaskDetailsAction(Action):

    def __init__(self, tasks_repo):
        self.tasks_repo = tasks_repo

    def process_request(self, request):
        task = self.tasks_repo.get(request.task_id)
        return ResponseSuccess(task)
