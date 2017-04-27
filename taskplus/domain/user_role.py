from taskplus.shared.domain_model import DomainModel


class UserRole(object):

    def __init__(self, name):
        self.name = name

    @classmethod
    def from_dict(cls, data):
        role = UserRole(name=data['name'])
        return role


DomainModel.register(UserRole)
