from taskplus.core.shared.request import Request
from taskplus.core.domain import Task, Statuses
from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess


class AddTaskAction(Action):

    def __init__(self, tasks_repo, users_repo, statuses_repo):
        super().__init__()
        self.tasks_repo = tasks_repo
        self.users_repo = users_repo
        self.statuses_repo = statuses_repo

    def process_request(self, request):
        creator = self.users_repo.one(request.creator_id)
        status = self.statuses_repo.one(Statuses.NEW)

        task = Task(name=request.name,
                    content=request.content,
                    status=status,
                    creator=creator)

        self._call_before_execution_hooks(dict(request=request, task=task))
        response = self.tasks_repo.save(task)
        self._call_after_execution_hooks(dict(request=request, task=response))

        return ResponseSuccess(response)


class AddTaskRequest(Request):

    def __init__(self, name, content, creator_id):
        super().__init__()
        self.name = name
        self.content = content
        self.creator_id = creator_id

    def _validate(self):
        self.errors = []

        if self.name is None:
            self._add_error('name', 'is required')
        elif isinstance(self.name, str) and not self.name.strip():
            self._add_error('name', 'is required')
        elif not isinstance(self.name, str):
            self._add_error('name', 'expected str, got {}({})'.format(
                self.name.__class__.__name__, self.name
            ))

        if self.content is None:
            self._add_error('content', 'is required')
        elif isinstance(self.content, str) and not self.content.strip():
            self._add_error('content', 'is required')
        elif not isinstance(self.content, str):
            self._add_error('content', 'expected str, got {}({})'.format(
                self.content.__class__.__name__, self.content
            ))

        if self.creator_id is None:
            self._add_error('creator_id', 'is required')
        elif not isinstance(self.creator_id, int):
            self._add_error('creator_id', 'expected int, got {}({})'.format(
                self.creator_id.__class__.__name__, self.creator_id
            ))
