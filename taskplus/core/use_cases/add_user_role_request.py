from taskplus.core.shared.request import Request


class AddUserRoleRequest(Request):

    def __init__(self, name=None):
        super().__init__()
        self.name = name

    @classmethod
    def from_dict(cls, data):
        request = AddUserRoleRequest()

        if 'name' in data:
            request.name = data['name']

        return request

    def _validate(self):
        if not self.name:
            self._add_error('name', 'is required')
