from taskplus.core.shared.domain_model import DomainModel


class UserRole(object):

    def __init__(self, name, id=None):
        self.name = name
        self.id = id


DomainModel.register(UserRole)
