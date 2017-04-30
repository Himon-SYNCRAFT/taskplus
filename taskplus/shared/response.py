class ResponseSuccess(object):

    def __init__(self, value=None):
        self.value = value

    def __nonzero__(self):
        return True

    __bool__ = __nonzero__


class ResponseFailure(object):

    PARAMETER_ERROR = 'PARAMETER_ERROR'
    SYSTEM_ERROR = 'SYSTEM_ERROR'
    RESOURCE_ERROR = 'RESOURCE_ERROR'

    def __init__(self, type_, message):
        self.type = type_
        self.message = self._format_message(message)

    @classmethod
    def build_resource_error(cls, message=None):
        return cls(cls.RESOURCE_ERROR, message)

    @classmethod
    def build_system_error(cls, message=None):
        return cls(cls.SYSTEM_ERROR, message)

    @classmethod
    def build_parameter_error(cls, message=None):
        return cls(cls.PARAMETER_ERROR, message)

    @classmethod
    def build_from_invalid_request(cls, invalid_request):
        errors = invalid_request.errors
        message = '\n'.join(['{}: {}'.format(parameter, message)
                             for parameter, message in errors])
        return cls(cls.PARAMETER_ERROR, message)

    def _format_message(self, msg):
        if isinstance(msg, Exception):
            return '{}: {}'.format(msg.__class__.__name__, msg)
        return msg

    @property
    def value(self):
        return {'type': self.type, 'message': self.message}

    def __nonzero__(self):
        return False

    __bool__ = __nonzero__
