from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.shared.action import Action
from collections import Mapping
from taskplus.core.shared.request import Request


class ListUserRolesAction(Action):

    def __init__(self, repo):
        super().__init__()
        self.repo = repo

    def process_request(self, request):
        self._call_before_execution_hooks(dict(request=request, roles=None))
        roles = self.repo.list(filters=request.filters)
        self._call_after_execution_hooks(dict(request=request, roles=roles))
        return ResponseSuccess(roles)


class ListUserRolesRequest(Request):

    def __init__(self, filters=None):
        super().__init__()

        if not filters:
            filters = None

        self.filters = filters
        self._validate()

    def _validate(self):
        self.errors = []

        if self.filters is None:
            return

        if not isinstance(self.filters, Mapping):
            parameter = 'filters'
            message = 'Is not iterable'
            self._add_error(parameter, message)
