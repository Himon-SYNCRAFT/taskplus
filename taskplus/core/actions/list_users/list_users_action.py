from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess


class ListUsersAction(Action):
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request):
        response = self.repo.list(filters=request.filters)
        return ResponseSuccess(response)
