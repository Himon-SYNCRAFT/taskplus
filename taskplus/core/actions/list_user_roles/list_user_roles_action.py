from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.shared.action import Action


class ListUserRolesAction(Action):

    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request):
        roles = self.repo.list(filters=request.filters)
        return ResponseSuccess(roles)
