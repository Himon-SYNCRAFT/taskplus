from operator import lt, le, eq, ne, ge, gt
from taskplus.core.shared.exceptions import NotAuthorized, InvalidOperatorError


class AuthorizationManager(object):

    def authorize(self, user, action, request):
        if not user.permissions:
            raise NotAuthorized

        permissions = [permission for permission in user.permissions
                       if permission.action == action.get_name()]

        if any([self._is_permitted(permission, user, request) is True
                for permission in permissions]):
            return

        raise NotAuthorized

    def _is_permitted(self, permission, user, request):
        if not permission.conditions:
            return True

        return all([condition.is_condition_met(user, request)
                    for condition in permission.conditions])


class Permission(object):

    def __init__(self, action, conditions=None):
        self.action = action
        self.conditions = conditions

        if conditions is None:
            self.conditions = []


class Condition(object):

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def is_condition_met(self, user, request):
        operator = self._parse_operator()
        left = self.left.split('.', maxsplit=1)
        right = self.right.split('.', maxsplit=1)

        if len(left) == 2:
            left, left_attribute = left
        else:
            left = left[0]
            left_attribute = None

        if len(right) == 2:
            right, right_attribute = right
        else:
            right = right[0]
            right_attribute = None

        if left == 'user':
            left = user
        elif left == 'request':
            left = request

        if right == 'user':
            right = user
        elif right == 'request':
            right = request

        if left_attribute:
            left = getattr(left, left_attribute)

        if right_attribute:
            right = getattr(right, right_attribute)

        return operator(left, right)

    def _parse_operator(self):
        allowed_operators = ['eq', 'lt', 'le', 'ne', 'ge', 'gt']

        if self.operator not in allowed_operators:
            raise InvalidOperatorError('Operator {} is not supported'.format(
                self.operator
            ))

        if self.operator == 'eq':
            return eq
        elif self.operator == 'lt':
            return lt
        elif self.operator == 'le':
            return le
        elif self.operator == 'ne':
            return ne
        elif self.operator == 'ge':
            return ge
        elif self.operator == 'gt':
            return gt

        return eq
