class NoResultFound(ValueError):

    def __init__(self, id, obj):
        self.message = 'No {} with id {}'.format(obj, id)
        self.id = id
        self.object_name = obj

    def __str__(self):
        return self.message


class NotAuthorized(Exception):
    pass


class InvalidOperatorError(ValueError):
    pass
