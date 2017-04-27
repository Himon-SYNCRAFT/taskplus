from taskplus.shared.response import ResponseSuccess


class ListUserRoles(object):

    def __init__(self, repo):
        self.repo = repo

    def execute(self, request):
        roles = self.repo.list()
        return ResponseSuccess(roles)
