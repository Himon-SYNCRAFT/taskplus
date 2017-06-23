from operator import eq, ne
from taskplus.core.shared.exceptions import NotAuthorized, InvalidOperatorError


class AuthorizationManager(object):
    user = None

    def authorize(self, action, context):
        if not self.user or not self.user.permissions:
            raise NotAuthorized(
                "You're not authorized to execute requested activity")

        permissions = (permission for permission in self.user.permissions
                       if permission.action == action)

        if any(permission.is_user_permitted(self.user, context)
               for permission in permissions):
            return

        raise NotAuthorized("You're not authorized to execute requested activity")


class Permission(object):

    def __init__(self, action, conditions=None):
        self.action = action
        self.conditions = conditions

        if conditions is None:
            self.conditions = []

    def is_user_permitted(self, user, context):
        if not self.conditions:
            return True

        return all(condition.is_met(user, context)
                   for condition in self.conditions)


class Condition(object):

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def is_met(self, user, context):
        operator = self._parse_operator()
        try:
            left = self._parse_operand(self.left, user, context)
            right = self._parse_operand(self.right, user, context)
        except AttributeError:
            return False

        return operator(left, right)

    def _parse_operand(self, operand, user, context):
        attributes = operand.split('.')[::-1]
        attribute = attributes.pop()

        if attribute == 'None':
            return None
        elif attribute.isnumeric():
            return int(attribute)
        elif attribute == 'user':
            attribute = user
        else:
            attribute = context[attribute]

        while attributes:
            next_attr = attributes.pop()
            attribute = getattr(attribute, next_attr)

        return attribute

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
