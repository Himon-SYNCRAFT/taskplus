from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.shared.request import Request


class UpdateTaskAction(Action):

    def __init__(self, tasks_repository):
        super().__init__()
        self.tasks_repository = tasks_repository

    def process_request(self, request):
        task = self.tasks_repository.one(request.id)
        self._call_before_execution_hooks(request, task)

        if request.name:
            task.name = request.name

        if request.content:
            task.content = request.content

        response = self.tasks_repository.update(task)
        self._call_after_execution_hooks(request, response)
        return ResponseSuccess(response)


class UpdateTaskRequest(Request):

    def __init__(self, id, name=None, content=None):
        super().__init__()

        self.id = id
        self.name = name
        self.content = content

        self._validate()

    def _validate(self):
        self.errors = []

        if self.id is None:
            self._add_error('id', 'is required')
        elif not isinstance(self.id, int):
            self._add_error('id', 'expected int, got {}({})'.format(
                self.id.__class__.__name__, self.id))

        if self.name is not None and not isinstance(self.name, str):
            self._add_error('name', 'expected str, got {}({})'.format(
                self.name.__class__.__name__, self.name))

        if self.content is not None and not isinstance(self.content, str):
            self._add_error('content', 'expected str, got {}({})'.format(
                self.content.__class__.__name__, self.content))
