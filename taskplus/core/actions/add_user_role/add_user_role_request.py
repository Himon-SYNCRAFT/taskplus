from taskplus.core.shared.request import Request


class AddUserRoleRequest(Request):

    def __init__(self, name):
        super().__init__()
        self.name = name
        self._validate()

    def _validate(self):
        self.errors = []

        if self.name is None:
            self._add_error('name', 'is required')
        elif isinstance(self.name, str) and not self.name.strip():
            self._add_error('name', 'is required')
        elif not isinstance(self.name, str):
            message = 'expected string, got {}({})'.format(
                self.name.__class__.__name__, self.name
            )
            self._add_error('name', message)
