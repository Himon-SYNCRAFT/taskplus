from taskplus.core.domain.user import User
from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess


class AddUserAction(Action):

    def __init__(self, users_repo, roles_repo):
        self.users_repo = users_repo
        self.roles_repo = roles_repo

    def process_request(self, request):
        role = self.roles_repo.get(request.role_id)
        user = User(name=request.name, role=role)

        response = self.users_repo.save(user)
        return ResponseSuccess(response)
