from collections import namedtuple


class Repository(object):

    def _parse_filters(self, filters=None):
        if not filters:
            return None

        allowed_operators = ['eq', 'lt', 'le', 'ne', 'ge', 'gt']
        result = []

        for key, value in filters.items():
            if '__' not in key:
                key = key + '__eq'

            key, operator = key.split('__')

            if operator not in allowed_operators:
                raise InvalidOperatorError('Operator {} is not supported'.format(
                    operator
                ))

            operator = '__{}__'.format(operator)

            result.append(Filter(key, operator, value))

        return result

    def one(self, id):
        raise NotImplementedError('one() not implemented by Repository class')

    def list(self, filters=None):
        raise NotImplementedError('list() not implemented by Repository class')

    def delete(self, id):
        raise NotImplementedError('delete() not implemented by Repository class')

    def update(self, domain_model):
        raise NotImplementedError('update() not implemented by Repository class')

    def save(self, domain_model):
        raise NotImplementedError('save() not implemented by Repository class')


class InvalidOperatorError(ValueError):
    pass


Filter = namedtuple('Filter', ['key', 'operator', 'value'])
