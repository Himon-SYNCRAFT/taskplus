from taskplus.core.shared.request import Request


class AddUserRequest(Request):

    def __init__(self, name, role_id):
        super().__init__()
        self.name = name
        self.role_id = role_id
        self._validate()

    def _validate(self):
        self.errors = []

        if self.name is None:
            self._add_error('name', 'is required')
        elif isinstance(self.name, str) and not self.name.strip():
            self._add_error('name', 'is required')
        elif not isinstance(self.name, str):
            message = 'expected str, got {}({})'.format(
                self.name.__class__.__name__, self.name
            )
            self._add_error('name', message)

        if not self.role_id:
            self._add_error('role_id', 'is required')
        elif not isinstance(self.role_id, int):
            message = 'expected int, got {}({})'.format(
                self.role_id.__class__.__name__, self.role_id
            )
            self._add_error('role_id', message)
