from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.shared.action import Action
from taskplus.core.shared.request import Request


class UnassignUserFromTaskAction(Action):

    def __init__(self, tasks_repo):
        self.tasks_repo = tasks_repo

    def process_request(self, request):
        task_id = request.task_id
        task = self.tasks_repo.one(task_id)

        task.doer = None
        response = self.tasks_repo.update(task)

        return ResponseSuccess(response)


class UnassignUserFromTaskRequest(Request):

    def __init__(self, task_id):
        super().__init__()
        self.task_id = task_id

    def _validate(self):
        self.errors = []

        if not self.task_id:
            self._add_error('task_id', 'is required')
        elif not isinstance(self.task_id, int):
            self._add_error('task_id', 'expected int, got {}({})'.format(
                self.task_id.__class__.__name__, self.task_id
            ))
