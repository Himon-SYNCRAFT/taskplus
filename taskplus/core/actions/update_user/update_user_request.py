from taskplus.core.shared.request import Request


class UpdateUserRequest(Request):

    def __init__(self, id, name=None, role_id=None):
        super().__init__()

        self.id = id
        self.name = name
        self.role_id = role_id

        self._validate()

    def _validate(self):
        self.errors = []

        if self.id is None:
            self._add_error('id', 'is required')
        elif not isinstance(self.id, int):
            self._add_error('id', 'expected int, got {}({})'.format(
                self.id.__class__.__name__, self.id))

        if self.name is not None and not isinstance(self.name, str):
            self._add_error('name', 'expected str, got {}({})'.format(
                self.name.__class__.__name__, self.name))

        if self.role_id is not None and not isinstance(self.role_id, int):
            self._add_error('role_id', 'expected int, got {}({})'.format(
                self.role_id.__class__.__name__, self.role_id))
