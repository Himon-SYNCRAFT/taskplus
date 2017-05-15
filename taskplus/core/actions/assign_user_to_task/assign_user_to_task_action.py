from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess


class AssignUserToTaskAction(Action):

    def __init__(self, tasks_repo, users_repo):
        self.tasks_repo = tasks_repo
        self.users_repo = users_repo

    def process_request(self, request):
        task_id = request.task_id
        user_id = request.user_id

        user = self.users_repo.get(user_id)
        task = self.tasks_repo.get(task_id)
        task.doer = user

        response = self.tasks_repo.update(task)
        return ResponseSuccess(response)
