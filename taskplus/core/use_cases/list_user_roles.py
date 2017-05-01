from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.shared.use_case import UseCase


class ListUserRoles(UseCase):

    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request):
        roles = self.repo.list(filters=request.filters)
        return ResponseSuccess(roles)
