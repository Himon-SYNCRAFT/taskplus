from taskplus.core.domain import TaskStatus
from taskplus.core.shared.domain_model import DomainModel


def test_task_status():
    status_id = 1
    status_name = 'canceled'
    status = TaskStatus(name=status_name, id=status_id)

    assert status.id == status_id
    assert status.name == status_name
    assert isinstance(status, DomainModel)
