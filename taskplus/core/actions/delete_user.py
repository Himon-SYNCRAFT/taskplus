from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.shared.request import Request


class DeleteUserAction(Action):

    def __init__(self, repo):
        super().__init__()
        self.repo = repo

    def process_request(self, request):
        user_id = request.id

        self._call_before_execution_hooks(request, None)
        response = self.repo.delete(user_id)
        self._call_after_execution_hooks(request, response)

        return ResponseSuccess(response)


class DeleteUserRequest(Request):

    def __init__(self, id):
        super().__init__()
        self.id = id
        self._validate()

    def _validate(self):
        self.errors = []

        if self.id is None:
            self._add_error('id', 'is required')
        elif not isinstance(self.id, int):
            self._add_error('id', 'expected int, got {}({})'.format(
                self.id.__class__.__name__, self.id))
