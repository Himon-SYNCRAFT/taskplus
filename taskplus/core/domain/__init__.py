from .user import User
from .user_role import UserRole
from .task_status import TaskStatus
from .task import Task


class Statuses(object):
    NEW = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    CANCELED = 4
