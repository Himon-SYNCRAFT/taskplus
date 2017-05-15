from taskplus.core.shared.domain_model import DomainModel


class Task(object):

    def __init__(self, name, content, status, creator, doer=None, id=None):
        self.name = name
        self.content = content
        self.status = status
        self.creator = creator
        self.doer = doer
        self.id = id


DomainModel.register(Task)
