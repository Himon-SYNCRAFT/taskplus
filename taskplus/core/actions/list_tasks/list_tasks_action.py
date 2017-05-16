from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess


class ListTasksAction(Action):
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request):
        response = self.repo.list(request)
        return ResponseSuccess(response)
