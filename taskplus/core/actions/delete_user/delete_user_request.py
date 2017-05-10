from taskplus.core.shared.request import Request


class DeleteUserRequest(Request):

    def __init__(self, id):
        super().__init__()
        self.id = id
        self._validate()

    def _validate(self):
        self.errors = []

        if self.id is None:
            self._add_error('id', 'is required')
        elif not isinstance(self.id, int):
            self._add_error('id', 'expected int, got {}({})'.format(
                self.id.__class__.__name__, self.id))
