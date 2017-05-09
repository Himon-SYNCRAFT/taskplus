from taskplus.core.shared.request import Request


class AddUserRoleRequest(Request):

    def __init__(self, name):
        super().__init__()
        self.name = name
        self._validate()

    def _validate(self):
        self.errors = []

        if not isinstance(self.name, str):
            message = 'expected string, got {}({})'.format(
                self.name.__class__.__name__, self.name
            )
            self._add_error('name', message)
        if not self.name:
            self._add_error('name', 'is required')
