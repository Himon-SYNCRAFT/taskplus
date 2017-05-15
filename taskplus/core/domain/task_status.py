from taskplus.core.shared.domain_model import DomainModel


class TaskStatus(object):

    def __init__(self, name, id=None):
        self.name = name
        self.id = id


DomainModel.register(TaskStatus)
