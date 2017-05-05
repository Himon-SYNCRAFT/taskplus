from collections import Mapping
from taskplus.core.shared.request import Request


class ListUserRolesRequest(Request):

    def __init__(self, filters=None):
        super().__init__()

        if not filters:
            filters = None

        self.filters = filters
        self._validate()

    @classmethod
    def from_dict(cls, data):
        if not data:
            data = None
        return ListUserRolesRequest(filters=data)

    def _validate(self):
        self.errors = []

        if self.filters is None:
            return

        if not isinstance(self.filters, Mapping):
            parameter = 'filters'
            message = 'Is not iterable'
            self._add_error(parameter, message)
