from enum import Enum

from taskplus.core.domain.user import User
from taskplus.core.domain.user_role import UserRole
from taskplus.core.domain.task_status import TaskStatus
from taskplus.core.domain.task import Task


class Statuses(Enum):
    NEW = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    CANCELED = 4
