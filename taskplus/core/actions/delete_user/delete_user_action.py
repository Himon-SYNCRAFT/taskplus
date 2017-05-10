from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess


class DeleteUserAction(Action):

    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request):
        user_id = request.id

        response = self.repo.delete(user_id)
        return ResponseSuccess(response)
