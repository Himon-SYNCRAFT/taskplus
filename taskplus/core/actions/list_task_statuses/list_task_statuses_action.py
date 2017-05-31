from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess


class ListTaskStatusesAction(Action):
    def __init__(self, repo):
        self.statuses_repo = repo

    def process_request(self, request):
        statuses = self.statuses_repo.list(filters=request.filters)
        return ResponseSuccess(statuses)
