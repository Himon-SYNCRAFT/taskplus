from taskplus.core.domain import Task, Statuses
from taskplus.core.shared.action import Action
from taskplus.core.shared.response import ResponseSuccess


class AddTaskAction(Action):

    def __init__(self, tasks_repo, users_repo, statuses_repo):
        self.tasks_repo = tasks_repo
        self.users_repo = users_repo
        self.statuses_repo = statuses_repo

    def process_request(self, request):
        creator = self.users_repo.get(request.creator_id)
        status = self.statuses_repo.get(Statuses.NEW)

        task = Task(name=request.name,
                    content=request.content,
                    status=status,
                    creator=creator)

        response = self.tasks_repo.save(task)
        return ResponseSuccess(response)
