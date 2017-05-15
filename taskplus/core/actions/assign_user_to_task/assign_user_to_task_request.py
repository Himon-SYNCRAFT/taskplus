from taskplus.core.shared.request import Request


class AssignUserToTaskRequest(Request):

    def __init__(self, task_id, user_id):
        super().__init__()
        self.task_id = task_id
        self.user_id = user_id

    def _validate(self):
        self.errors = []

        if not self.task_id:
            self._add_error('task_id', 'is required')
        elif not isinstance(self.task_id, int):
            self._add_error('task_id', 'expected int, got {}({})'.format(
                self.task_id.__class__.__name__, self.task_id
            ))

        if not self.user_id:
            self._add_error('user_id', 'is required')
        elif not isinstance(self.user_id, int):
            self._add_error('user_id', 'expected int, got {}({})'.format(
                self.user_id.__class__.__name__, self.user_id
            ))
