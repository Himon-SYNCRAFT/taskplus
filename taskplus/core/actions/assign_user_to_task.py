from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.shared.request import Request


class AssignUserToTaskAction(Action):

    def __init__(self, tasks_repo, users_repo):
        super().__init__()
        self.tasks_repo = tasks_repo
        self.users_repo = users_repo

    def process_request(self, request):
        task_id = request.task_id
        user_id = request.user_id

        user = self.users_repo.one(user_id)
        task = self.tasks_repo.one(task_id)
        self._call_before_execution_hooks(request, task)

        task.doer = user
        response = self.tasks_repo.update(task)
        self._call_after_execution_hooks(request, task)

        return ResponseSuccess(response)


class AssignUserToTaskRequest(Request):

    def __init__(self, task_id, user_id):
        super().__init__()
        self.task_id = task_id
        self.user_id = user_id

    def _validate(self):
        self.errors = []

        if not self.task_id:
            self._add_error('task_id', 'is required')
        elif not isinstance(self.task_id, int):
            self._add_error('task_id', 'expected int, got {}({})'.format(
                self.task_id.__class__.__name__, self.task_id
            ))

        if not self.user_id:
            self._add_error('user_id', 'is required')
        elif not isinstance(self.user_id, int):
            self._add_error('user_id', 'expected int, got {}({})'.format(
                self.user_id.__class__.__name__, self.user_id
            ))
