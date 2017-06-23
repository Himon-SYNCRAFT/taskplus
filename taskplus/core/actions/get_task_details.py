from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.shared.request import Request


class GetTaskDetailsAction(Action):

    def __init__(self, tasks_repo):
        super().__init__()
        self.tasks_repo = tasks_repo

    def process_request(self, request):
        self._call_before_execution_hooks(dict(request=request, task=None))
        task = self.tasks_repo.one(request.task_id)
        self._call_after_execution_hooks(dict(request=request, task=task))

        return ResponseSuccess(task)


class GetTaskDetailsRequest(Request):

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
