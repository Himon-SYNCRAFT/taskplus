from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess
from collections import Mapping
from taskplus.core.shared.request import Request


class ListTaskStatusesAction(Action):
    def __init__(self, repo):
        self.statuses_repo = repo

    def process_request(self, request):
        statuses = self.statuses_repo.list(filters=request.filters)
        return ResponseSuccess(statuses)


class ListTaskStatusesRequest(Request):

    def __init__(self, filters=None):
        super().__init__()
        self.filters = filters

        if not filters:
            self.filters = None

        self._validate()

    def _validate(self):
        self.errors = []

        if self.filters is None:
            return

        if not isinstance(self.filters, Mapping):
            parameter = 'filters'
            message = 'is not iterable'
            self._add_error(parameter, message)
