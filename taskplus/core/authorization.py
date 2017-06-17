from operator import eq, ne
from taskplus.core.shared.exceptions import NotAuthorized, InvalidOperatorError


class AuthorizationManager(object):
    user = None

    def authorize(self, action, data):
        if not self.user or not self.user.permissions:
            raise NotAuthorized

        permissions = (permission for permission in self.user.permissions
                       if permission.action == action)

        if any(permission.is_user_permitted(self.user, data)
               for permission in permissions):
            return

        raise NotAuthorized


class Permission(object):

    def __init__(self, action, conditions=None):
        self.action = action
        self.conditions = conditions

        if conditions is None:
            self.conditions = []

    def is_user_permitted(self, user, data):
        if not self.conditions:
            return True

        return all(condition.is_met(user, data)
                   for condition in self.conditions)


class Condition(object):

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def is_met(self, user, data):
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
        elif left.isnumeric():
            left = int(left)
        else:
            left = data[left]

        if right == 'user':
            right = user
        elif right.isnumeric():
            right = int(right)
        else:
            right = data[right]

        if left_attribute:
            left = getattr(left, left_attribute)

        if right_attribute:
            right = getattr(right, right_attribute)

        return operator(left, right)

    def _parse_operator(self):
        allowed_operators = ['eq', 'ne']

        if self.operator not in allowed_operators:
            raise InvalidOperatorError('Operator {} is not supported'.format(
                self.operator
            ))

        if self.operator == 'eq':
            return eq
        elif self.operator == 'ne':
            return ne

        return eq
