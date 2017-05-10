from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess


class UpdateUserAction(Action):

    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request):
        user_id = request.id
        user = self.repo.get(user_id)

        if request.name:
            user.name = request.name

        if request.role_id:
            user.role_id = request.role_id

        response = self.repo.update(user)
        return ResponseSuccess(response)
