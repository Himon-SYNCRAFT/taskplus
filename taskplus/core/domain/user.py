from taskplus.core.shared.domain_model import DomainModel


class User(object):

    def __init__(self, name, role, id=None):
        self.name = name
        self.role = role
        self.id = id


DomainModel.register(User)
