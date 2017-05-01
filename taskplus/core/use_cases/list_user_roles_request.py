from collections import Mapping
from taskplus.core.shared.request import ValidRequest, InvalidRequest


class ListUserRolesRequest(ValidRequest):

    def __init__(self, filters=None):
        self.filters = filters

    @classmethod
    def from_dict(cls, data):
        invalid_request = InvalidRequest()

        if 'filters' in data and not isinstance(data['filters'], Mapping):
            parameter = 'filters'
            message = 'Is not iterable'
            invalid_request.add_error(parameter, message)

        if invalid_request.has_errors():
            return invalid_request

        return ListUserRolesRequest(filters=data.get('filters', None))

    def __nonzero__(self):
        return True
