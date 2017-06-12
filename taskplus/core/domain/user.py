from taskplus.core.shared.domain_model import DomainModel


class User(object):

    def __init__(self, name, roles, id=None):
        self.name = name
        self.roles = roles
        self.id = id


DomainModel.register(User)
