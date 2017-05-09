from taskplus.core.shared.response import ResponseSuccess
from taskplus.core.shared.use_case import UseCase


class UpdateUserRole(UseCase):

    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request):
        role = self.repo.one(id=request.id)

        if request.name:
            role.name = request.name

        self.repo.update(role)
        return ResponseSuccess(role)
