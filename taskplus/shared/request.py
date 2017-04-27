from collections import namedtuple


RequestError = namedtuple('RequestError', ['parameter', 'message'])


class InvalidRequest(object):

    def __init__(self):
        self._errors = []

    def add_error(self, parameter, message):
        error = RequestError(parameter=parameter, message=message)
        self._errors.append(error)

    def has_errors(self):
        return len(self._errors) > 0

    def __nonzero__(self):
        return False

    __bool__ = __nonzero__


class ValidRequest(object):

    @classmethod
    def from_dict(cls, data):
        raise NotImplementedError

    def __nonzero__(self):
        return True

    __bool__ = __nonzero__
