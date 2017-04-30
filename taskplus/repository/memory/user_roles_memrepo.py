from taskplus.domain.user_role import UserRole


class UserRolesRepo(object):

    def __init__(self, entries=None):
        self._entries = []
        if entries:
            self._entries.extend(entries)

    def _check(self, element, key, value):
        if '__' not in key:
            key = key + '__eq'

        key, operator = key.split('__')

        if operator != 'eq':
            raise ValueError('Operator {} is not supported'.format(operator))

        operator = '__{}__'.format(operator)

        return getattr(element[key], operator)(value)

    def list(self, filters=None):
        if not filters:
            return self._entries

        result = []
        result.extend(self._entries)

        for key, value in filters.items():
            result = [e for e in result if self._check(e, key, value)]

        return [UserRole.from_dict(item) for item in result]
