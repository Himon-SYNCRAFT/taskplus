from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.shared.request import Request


class GetUserDetailsAction(Action):

    def __init__(self, users_repo):
        super().__init__()
        self.users_repo = users_repo

    def process_request(self, request):
        self._call_before_execution_hooks(request, None)
        user = self.users_repo.one(request.user_id)
        self._call_after_execution_hooks(request, user)

        return ResponseSuccess(user)


class GetUserDetailsRequest(Request):

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    def _validate(self):
        self.errors = []

        if not self.user_id:
            self._add_error('user_id', 'is required')
        elif not isinstance(self.user_id, int):
            self._add_error('user_id', 'expected int, got {}({})'.format(
                self.user_id.__class__.__name__, self.user_id
            ))
