from collections import namedtuple


RequestError = namedtuple('RequestError', ['parameter', 'message'])


class Request(object):

    def __init__(self):
        self.errors = []

    def _add_error(self, parameter, message):
        error = RequestError(parameter=parameter, message=message)
        self.errors.append(error)

    def is_valid(self):
        self._validate()
        return len(self.errors) == 0

    def _validate(self):
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data):
        raise NotImplementedError
