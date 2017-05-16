from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess


class GetUserDetailsAction(Action):

    def __init__(self, users_repo):
        self.users_repo = users_repo

    def process_request(self, request):
        user = self.users_repo.get(request.user_id)
        return ResponseSuccess(user)
