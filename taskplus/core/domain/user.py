from taskplus.core.shared.domain_model import DomainModel


class User(object):

    def __init__(self, name, roles, permissions=None, id=None):
        self.name = name
        self.roles = roles
        self.id = id
        self.permissions = permissions

        if permissions is None:
            self.permissions = []


DomainModel.register(User)
